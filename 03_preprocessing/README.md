# 03 — Pre-processing

Building each study's object from the raw deposit, and quality control.

Planned steps:

1. Per-study object build (raw counts, gene IDs harmonised, metadata from `02_`).
2. Compartment-level labels (L0) used to stratify QC.
3. QC metrics and MAD-based filtering per study × compartment.
4. Doublet detection (Scrublet / scDblFinder) and ambient RNA (decontX).
5. Export of the QC-passed objects as input to integration.

Input: `01_download/` output and `02_metadata_curation/`. Output: QC-passed per-study
objects (outside git).

Status: to be filled.
