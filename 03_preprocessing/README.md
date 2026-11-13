# 03 — Pre-processing

From the downloaded deposits to quality-controlled objects, one per study.

## 1. Build the per-study objects

```bash
python 03_preprocessing/scripts/build_objects.py                         # all 28 studies
python 03_preprocessing/scripts/build_objects.py --study gribben_2024    # or some
```

Reads `<data>/01_raw/` (see `01_download/`) and writes `<data>/03_objects/per_study/<study>.h5ad`:

- `X`: raw counts of every deposited cell of the in-scope samples (cells with zero counts dropped), every deposited gene;
  `var['gene_id']` where the deposit gives one;
- `obs`: `study`, `atlas_sample_id`, `suspension_type`, `source_sample_id` and the authors' per-cell metadata as
  deposited.

Each study has a short recipe in [`scripts/recipes/`](scripts/recipes/) that says how its deposit is read. The
in-scope samples, and the number of cells each must keep, come from
[`02_metadata_curation/tables/samples.csv`](../02_metadata_curation/tables/samples.csv). The build stops if any sample
differs. Studies deposited as Seurat objects (`.rds`) are read through R with Seurat installed: `Rscript` on `PATH`,
or set `MASLD_RSCRIPT=/path/to/Rscript`.

Objects whose recipe is in the folder have been rebuilt from the downloads and compared cell by cell with the atlas
objects (same cells, samples, genes and counts). Recipes for the remaining studies are being added.

## 2. Next

Compartment-level labels used to stratify QC (`04_annotation/`), then QC metrics and thresholds per study × chemistry
× compartment, doublets, ambient RNA (decontX), and the QC ridge plots.
