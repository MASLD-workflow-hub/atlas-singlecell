"""dudek_2021 (GEO GSE159977): per-sample 10x triplets in GSE159977_RAW.tar; the authors' per-cell metadata
(GSE159977_scRNA_metadata.csv.gz) lists the cells they called, and only those are kept.
Cell name = <sample>_<barcode>; source_sample_id = the GSM of the tar member."""
import re

import anndata as ad
import pandas as pd

from readers import read_triplet, tar_triplets, to_anndata

ACC = 'GSE159977'


def build(raw):
    tf, groups = tar_triplets(raw / ACC / f'{ACC}_RAW.tar')
    parts = []
    for stem, g in sorted(groups.items()):
        X, bc, ft = read_triplet(tf, g)
        gsm, sample = re.match(r'^(GSM\d+)[_-](.+)$', stem).groups()
        obs = pd.DataFrame({'sample': sample, 'source_sample_id': gsm}, index=pd.Index([f'{sample}_{b}' for b in bc]))
        parts.append(to_anndata(X, obs, ft))
    a = ad.concat(parts, join='outer', index_unique=None, merge='first')
    md = pd.read_csv(raw / ACC / f'{ACC}_scRNA_metadata.csv.gz')
    md.index = pd.Index(md['sample_ID'].astype(str) + '_' + md['cellID'].astype(str))
    a = a[a.obs_names.isin(md.index)].copy()
    a.obs = a.obs.join(md[~md.index.duplicated()])
    return a
