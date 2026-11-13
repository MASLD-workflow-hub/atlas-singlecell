# MASLD single-cell liver atlas

Code, notebooks and the study table behind the MASLD single-cell liver atlas.

The atlas covers 28 published human liver single-cell and single-nucleus RNA-seq studies
(10x Genomics; control and MASLD tissue only): 2,186,795 deposited cells, of which 1,855,148 cells from 337 donors
and 405 samples form the atlas (Table 1, [`00_data_table/`](00_data_table/)).
This repository holds **code and small tables only**. Count matrices, `h5ad` objects and
models are not tracked: `01_download/` fetches the public data (about 84 GB) into a data folder
of your choice.

## Layout

| folder | contents |
|---|---|
| [`00_data_table/`](00_data_table/) | Table 1: the studies, samples and cell counts in the atlas |
| [`01_download/`](01_download/) | scripts that fetch the raw deposited data (GEO, ArrayExpress, Zenodo, ...) |
| [`02_metadata_curation/`](02_metadata_curation/) | how sample, donor and clinical metadata were curated and harmonised (disease stage, MONDO, Cell Ontology) |
| [`03_preprocessing/`](03_preprocessing/) | per-study object build, quality control, doublet and ambient-RNA handling |
| [`04_annotation/`](04_annotation/) | compartment (L0/L1) and fine cell-type annotation |
| [`05_integration/`](05_integration/) | atlas integration (scVI / Harmony), benchmarking, final model |
| [`environment/`](environment/) | conda environment specs needed to rerun the code |
| [`tools/`](tools/) | data-folder helpers (`init_data_dir.py`, `paths.py`) and the payload check before commits |
| [`config/`](config/) | `paths.example.yaml`; your own `paths.yaml` (not tracked) |

Each numbered folder has `scripts/` (plain `.py` / `.R` / `.sh`) and `notebooks/`
(`.ipynb`, committed with outputs where these are small), plus a `README.md` that states
the inputs, the outputs and the run order.

The numbers follow the order of the steps. In practice, compartment-level annotation
(L0/L1) is an input to QC, and fine annotation runs on the integrated object. Each
README states which earlier steps it depends on.

## Quick start: set up and run

```bash
git clone https://github.com/MASLD-workflow-hub/atlas-singlecell.git
cd atlas-singlecell
python tools/init_data_dir.py /path/to/masld_data   # 1. create your data folder (any location, outside the repo)
# 2. create the conda environments: environment/README.md
# 3. download the raw data into the data folder:   01_download/
python tools/init_data_dir.py --check               #    which of the 28 studies are on disk
# 4. run the steps in order: 02_metadata_curation/ -> 03_preprocessing/ -> 04_annotation/ -> 05_integration/
```

Step 1 creates the folder layout and records the location in `config/paths.yaml`. Every script finds the data
through that file, or through `MASLD_DATA_DIR` if that is set. The layout, and which step reads and writes each folder,
is described in [`DATA_LAYOUT.md`](DATA_LAYOUT.md).

## Conventions

- Scripts find the data folder with `tools/paths.py` (`config/paths.yaml` or `MASLD_DATA_DIR`) and take other inputs as
  arguments. Paths are never hard-coded as `/home/...`.
- File names start with the step number, for example `03_01_qc_metrics.py`.
- Nothing above a few MB goes into git. Run `tools/check_payload.sh` before pushing.

## Releases

See [`CHANGELOG.md`](CHANGELOG.md). Releases are tagged `vMAJOR.MINOR.PATCH`.

## Licence

[PolyForm Noncommercial License 1.0.0](https://polyformproject.org/licenses/noncommercial/1.0.0)
(see [`LICENSE`](LICENSE)).

You may use, change and share this code for any **non-commercial** purpose. That covers
personal research and study, and use by universities, public research institutes,
hospitals, charities and government bodies, whoever funds them. Commercial use needs a
separate licence: contact the maintainers.

Required Notice: Copyright (c) 2026 MASLD-workflow-hub (https://github.com/MASLD-workflow-hub)
