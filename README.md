# MASLD single-cell liver atlas

Code, notebooks and the study table behind the v1 MASLD single-cell liver atlas.

The atlas covers 28 published human liver single-cell and single-nucleus RNA-seq studies
(10x Genomics; control and MASLD tissue only), 2,186,795 deposited cells (Table 1 v6).
This repository holds **code and small tables only**. Count matrices, `h5ad` objects and
models are not tracked, and the download scripts fetch the raw data again from the
public archives.

## Layout

| folder | contents |
|---|---|
| [`00_data_table/`](00_data_table/) | Table 1: the studies, samples and cell counts in the v1 atlas |
| [`01_download/`](01_download/) | scripts that fetch the raw deposited data (GEO, ArrayExpress, Zenodo, ...) |
| [`02_metadata_curation/`](02_metadata_curation/) | how sample, donor and clinical metadata were curated and harmonised (disease stage, MONDO, Cell Ontology) |
| [`03_preprocessing/`](03_preprocessing/) | per-study object build, quality control, doublet and ambient-RNA handling |
| [`04_annotation/`](04_annotation/) | compartment (L0/L1) and fine cell-type annotation |
| [`05_integration/`](05_integration/) | atlas integration (scVI / Harmony), benchmarking, final model |
| [`environment/`](environment/) | conda environment specs needed to rerun the code |
| [`tools/`](tools/) | repository helpers (payload check before commits) |

Each numbered folder has `scripts/` (plain `.py` / `.R` / `.sh`) and `notebooks/`
(`.ipynb`, committed with outputs where these are small), plus a `README.md` that states
the inputs, the outputs and the run order.

The numbers follow the order of the steps. In practice, compartment-level annotation
(L0/L1) is an input to QC, and fine annotation runs on the integrated object. Each
README states which earlier steps it depends on.

## Conventions

- Scripts take input and output paths as arguments or from one config file, never as
  hard-coded `/home/...` paths.
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
