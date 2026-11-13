# Data folder: where your downloaded data live

The repository holds code and small tables only. The data (raw downloads, `h5ad` objects, models) live in **one
folder of your choice outside the repository**, called the *data folder* below. Every script and notebook finds it in
the same way, so you set it once.

## 1. Choose a folder and create the layout

Pick a disk with room for the raw downloads and the objects (the downloads take about 84 GB; plan for about three times that with the objects).
Then, from the repository root:

```bash
python tools/init_data_dir.py /path/to/masld_data
```

This creates the folders below (it never deletes or overwrites anything) and writes `config/paths.yaml`, which
records where the data folder is. `config/paths.yaml` is personal and is not tracked by git.

## 2. How the code finds the data folder

In this order:

1. the environment variable `MASLD_DATA_DIR`, if it is set (useful on a cluster or in a job script):
   `export MASLD_DATA_DIR=/path/to/masld_data`
2. `data_dir:` in `config/paths.yaml` (written by step 1; the template is `config/paths.example.yaml`).

In Python (scripts and notebooks):

```python
import sys; sys.path.insert(0, '<path to the repository>')
from tools.paths import data_dir, path

data_dir()                               # /path/to/masld_data
path('raw', 'GSE212837')                 # /path/to/masld_data/01_raw/GSE212837
path('per_study', 'wang_2023.h5ad')      # /path/to/masld_data/03_objects/per_study/wang_2023.h5ad
```

In a shell script: `DATA=$(python tools/paths.py)`.

## 3. Layout

The numbers match the step folders of the repository: step `0N_*` writes into `0N_*` of the data folder and reads
only from earlier steps.

```
masld_data/
├── 01_raw/                      written by 01_download: files exactly as deposited, one folder per accession
│   └── <accession>/             e.g. GSE212837/, zenodo-17735506/, cxg-059202e1-.../ (which study uses which file:
│                                01_download/download_manifest.csv)
├── 02_metadata/                 written by 02_metadata_curation: per-sample and per-donor tables, MONDO / CL maps
├── 03_objects/                  written by 03_preprocessing
│   ├── per_study/<study>.h5ad   one object per study: raw counts, harmonised genes, curated obs
│   ├── qc/<study>.h5ad          QC-passed cells, decontX counts in layers['decontx']
│   └── sidecars/                cells set aside, with the reason (doublets, low quality); nothing is deleted
├── 04_annotation/               written by 04_annotation: per-cell label tables (L0/L1, compartment, fine labels)
├── 05_integration/              written by 05_integration
│   ├── atlas.h5ad               the integrated object (latent embedding in obsm)
│   └── models/<model>/          trained scVI models
└── logs/                        run logs
```

`<study>` (used from `03_objects/` on) is the `Dataset` column of [`00_data_table/table1_studies.csv`](00_data_table/table1_studies.csv)
(e.g. `andrews_2022`, `jimenez-gracia_2026`).

## 4. Checks

- `python tools/init_data_dir.py --check` lists, for each of the 28 studies, whether all its files of the download
  manifest are in `01_raw/` with the right size.
- Downloads that are already on disk are not fetched again (see `01_download/`).
