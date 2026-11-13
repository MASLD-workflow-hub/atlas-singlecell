"""Readers shared by the study recipes."""
import gzip
import io
import re
import tarfile

import anndata as ad
import numpy as np
import pandas as pd
import scipy.io
import scipy.sparse as sp

TRIPLET = re.compile(r'^(?P<stem>.+?)[_-](?P<kind>barcodes|features|genes|matrix)\.(tsv|mtx)(\.gz)?$')


def tar_triplets(tar_path):
    """{stem: {'barcodes'|'features'|'matrix': member name}} for every 10x triplet inside a tar."""
    tf = tarfile.open(tar_path)
    groups = {}
    for n in tf.getnames():
        m = TRIPLET.match(n.rsplit('/', 1)[-1])
        if m:
            kind = 'features' if m.group('kind') in ('features', 'genes') else m.group('kind')
            groups.setdefault(m.group('stem'), {})[kind] = n
    return tf, groups


def _member(tf, name):
    raw = tf.extractfile(name).read()
    return gzip.open(io.BytesIO(raw)) if name.endswith('.gz') else io.BytesIO(raw)


def read_triplet(tf, g):
    """One 10x triplet -> (counts cells x genes, barcodes, features table)."""
    X = sp.csr_matrix(scipy.io.mmread(_member(tf, g['matrix'])).T.astype(np.float32))
    bc = pd.read_csv(_member(tf, g['barcodes']), header=None)[0].astype(str)
    ft = pd.read_csv(_member(tf, g['features']), sep='\t', header=None)
    return X, bc, ft


def to_anndata(X, obs, ft):
    """AnnData with gene symbols as var names (made unique) and the deposit's gene id in var['gene_id']."""
    sym = (ft[1] if ft.shape[1] > 1 else ft[0]).astype(str)
    var = pd.DataFrame(index=pd.Index(sym.values))
    if ft.shape[1] > 1:
        var['gene_id'] = ft[0].astype(str).values
    a = ad.AnnData(X=X, obs=obs, var=var)
    a.var_names_make_unique()
    return a


def from_seurat(rds, double_gz=True):
    """Counts (RNA assay, 'counts') and meta.data of a Seurat .rds, read through R.

    Needs R with Seurat and Matrix: the Rscript on PATH, or the one named by the environment variable MASLD_RSCRIPT.
    GEO's .rds.gz files are compressed twice (saveRDS, then GEO), hence gzcon(gzfile()). The sparse matrix is passed
    to Python as raw binary vectors, which is fast for matrices with hundreds of millions of non-zeros."""
    import os
    import subprocess
    import tempfile
    r = r'''
    suppressPackageStartupMessages({library(Seurat); library(Matrix)})
    o <- readRDS(%s)
    m <- GetAssayData(o, assay = "RNA", layer = "counts")
    d <- "%s"
    writeBin(as.integer(m@i), file.path(d, "i.bin"), size = 4)
    writeBin(as.integer(m@p), file.path(d, "p.bin"), size = 4)
    writeBin(as.double(m@x),  file.path(d, "x.bin"), size = 8)
    write.csv(data.frame(gene = rownames(m)), file.path(d, "var.csv"), row.names = FALSE)
    md <- o@meta.data; md$cell <- rownames(md)
    write.csv(md, file.path(d, "obs.csv"), row.names = FALSE, na = "")
    '''
    src = f'gzcon(gzfile("{rds}", "rb"))' if double_gz else f'"{rds}"'
    rscript = os.environ.get('MASLD_RSCRIPT', 'Rscript')
    with tempfile.TemporaryDirectory(dir=os.environ.get('MASLD_TMP')) as d:
        subprocess.run([rscript, '--vanilla', '-e', r % (src, d)], check=True)
        var = pd.read_csv(f'{d}/var.csv')
        obs = pd.read_csv(f'{d}/obs.csv', low_memory=False)
        i = np.fromfile(f'{d}/i.bin', dtype=np.int32)
        p = np.fromfile(f'{d}/p.bin', dtype=np.int32)
        x = np.fromfile(f'{d}/x.bin', dtype=np.float64).astype(np.float32)
    X = sp.csr_matrix((x, i, p), shape=(len(obs), len(var)))   # dgCMatrix genes x cells = CSR cells x genes
    obs = obs.set_index(obs['cell'].astype(str)).drop(columns=['cell'])
    obs.index.name = None
    for c in obs.columns:                                        # CSV round trip: keep text columns as text
        if obs[c].dtype == object:
            obs[c] = obs[c].fillna('').astype(str)
    a = ad.AnnData(X=X, obs=obs, var=pd.DataFrame(index=pd.Index(var['gene'].astype(str))))
    a.var_names_make_unique()
    return a
