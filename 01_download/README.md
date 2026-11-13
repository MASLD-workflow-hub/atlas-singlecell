# 01 — Download

Fetches the public files the 28 studies are built from into your data folder (see [`../DATA_LAYOUT.md`](../DATA_LAYOUT.md)).

```bash
python tools/init_data_dir.py /path/to/masld_data      # once: create the data folder
python 01_download/scripts/download.py --dry-run       # what will be fetched, and how much
python 01_download/scripts/download.py                 # everything: 81 files, about 84 GB
python 01_download/scripts/download.py --study wang_2023 gribben_2024   # or some studies only
python tools/init_data_dir.py --check                  # which studies are complete
```

Standard Python 3 only, no extra packages. Run it in `screen` / `tmux` or a batch job: the largest file is 17 GB.

## What is fetched

[`download_manifest.csv`](download_manifest.csv) has one row per file and study:

| column | meaning |
|---|---|
| `study` | the `Dataset` of `00_data_table/table1_studies.csv` |
| `role` | `counts` = the deposit the study's object is built from; `author_metadata` = authors' files that carry per-cell labels, per-cell patient assignment or sample tables |
| `repository`, `accession`, `file`, `url` | where it comes from (GEO, Zenodo, CELLxGENE) |
| `bytes`, `sha256`, `md5`, `version` | the expected size; sha256 of the file we used; the publisher's md5 (Zenodo); the CELLxGENE dataset version |
| `target` | where it is saved, under `<data folder>/01_raw/` |

Files that two studies share (the HLiCA release for henderson_unpublished and thomann_2026, one CELLxGENE file for the
two edgar_2025 arms) are downloaded once. `--role counts` skips the author files (27 GB, mostly two large author objects
used only for labels and patient assignment).

## Checks

- A file counts as complete when its size matches the manifest. After a download its sha256 (or the publisher's md5)
  is checked, and on a mismatch the run stops with the file kept as `.bad`.
- An interrupted download resumes from its `.part` file. A complete file is never fetched again.
- `--verify` re-checksums files already on disk.
- Every log is written to `<data folder>/logs/download_<time>.tsv`.

Repositories can change. If a URL stops working or a checksum no longer matches, please open an issue.
