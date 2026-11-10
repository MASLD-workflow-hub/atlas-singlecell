# 01 — Download scripts for the raw data

Scripts that fetch each study's deposited data from the public archive (GEO, ArrayExpress,
Zenodo, CELLxGENE, the authors' own sites) into a local data directory that is not tracked.

- `scripts/`: one entry point that reads the accession list in `00_data_table/` and
  per-source fetchers.
- Downloads are checked against file sizes or checksums. Files already on disk are not
  fetched again.

Input: `00_data_table/table1_studies.csv`. Output: `<data_dir>/raw/<study>/` (outside git).

Status: to be filled.
