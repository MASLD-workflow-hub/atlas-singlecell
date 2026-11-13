#!/usr/bin/env python
"""Build one object per study from the downloaded deposits (see 03_preprocessing/README.md).

  python 03_preprocessing/scripts/build_objects.py                     # all 28 studies
  python 03_preprocessing/scripts/build_objects.py --study dudek_2021  # one or more studies

For each study, recipes/<study>.py reads the files in <data>/01_raw/ and returns every deposited cell with raw counts,
the authors' per-cell metadata and the deposit's sample name (`source_sample_id`). This script then keeps the in-scope
samples of 02_metadata_curation/tables/samples.csv, drops cells with zero counts, adds `study`, `atlas_sample_id` and
`suspension_type`, checks the cells per sample against the table, and writes <data>/03_objects/per_study/<study>.h5ad.
An existing object is not rebuilt unless --force is given."""
import argparse
import importlib.util
import sys
import time
from pathlib import Path

import anndata as ad
import numpy as np
import pandas as pd
import scipy.sparse as sp

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(REPO))
from tools.paths import path  # noqa: E402

SAMPLES = REPO / '02_metadata_curation' / 'tables' / 'samples.csv'


sys.path.insert(0, str(HERE / "recipes"))


def recipe(study):
    spec = importlib.util.spec_from_file_location(f'recipe_{study}', HERE / 'recipes' / f'{study.replace("-", "_")}.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def finish(a, study, samples):
    """Keep the in-scope samples, drop empty cells, add the atlas sample fields, check cells per sample."""
    smp = samples[samples.study == study].set_index('source_sample_id')
    src = a.obs['source_sample_id'].astype(str)
    unknown = sorted(set(src) - set(smp.index))
    if unknown:
        raise SystemExit(f'{study}: deposit samples missing from samples.csv: {unknown[:5]}')
    keep = src.map(smp.in_scope).isin(['yes', 'partly']).to_numpy()
    if 'keep_partly' in a.obs:                       # set by recipes whose pooled libraries are kept in part
        keep &= np.where(src.map(smp.in_scope).eq('partly').to_numpy(), a.obs['keep_partly'].to_numpy(bool), True)
        a.obs = a.obs.drop(columns='keep_partly')
    keep &= np.asarray(a.X.sum(axis=1)).ravel() > 0
    a = a[keep].copy()
    src = a.obs['source_sample_id'].astype(str)
    a.obs.insert(0, 'study', study)
    a.obs.insert(1, 'atlas_sample_id', src.map(smp.atlas_sample_id).values)
    a.obs.insert(2, 'suspension_type', src.map(smp.suspension_type).values)
    want = smp[smp.in_scope != 'no'].set_index('atlas_sample_id').n_cells_kept
    got = a.obs.atlas_sample_id.value_counts().reindex(want.index).fillna(0).astype(int)
    if not got.equals(want.astype(int)):
        diff = pd.DataFrame({'expected': want, 'built': got})
        raise SystemExit(f'{study}: cells per sample differ from samples.csv:\n{diff[diff.expected != diff.built]}')
    a.X = sp.csr_matrix(a.X, dtype=np.float32)
    a.obs_names.name = a.var_names.name = None
    for c in a.obs.columns:                          # plain strings for h5ad
        if a.obs[c].dtype == object:
            a.obs[c] = a.obs[c].astype(str)
    return a


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--study', nargs='+')
    ap.add_argument('--force', action='store_true', help='rebuild objects that already exist')
    args = ap.parse_args()
    samples = pd.read_csv(SAMPLES, dtype={'n_cells_kept': int}, keep_default_na=False)
    studies = args.study or sorted(samples.study.unique())
    raw, out = path('raw'), path('per_study')
    out.mkdir(parents=True, exist_ok=True)
    for study in studies:
        dest = out / f'{study}.h5ad'
        if dest.exists() and not args.force:
            print(f'{study}: {dest} exists, skipped (--force to rebuild)'); continue
        t0 = time.time()
        print(f'{study}: reading the deposit')
        a = recipe(study).build(raw)
        a = finish(a, study, samples)
        a.uns['build'] = {'study': study, 'recipe': f'03_preprocessing/scripts/recipes/{study.replace("-", "_")}.py'}
        tmp = dest.with_suffix('.h5ad.part')
        a.write_h5ad(tmp, compression='lzf')
        tmp.rename(dest)
        print(f'{study}: {a.n_obs:,} cells x {a.n_vars:,} genes, {a.obs.atlas_sample_id.nunique()} samples '
              f'-> {dest} ({time.time() - t0:.0f} s)')


if __name__ == '__main__':
    main()
