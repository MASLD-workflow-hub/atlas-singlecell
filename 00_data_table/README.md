# 00 — Data table

Table 1 of the atlas: the 28 studies, one row per study.

| file | contents |
|---|---|
| [`table1_studies.csv`](table1_studies.csv) | publication (DOI, journal, year), accession(s), tissue fraction, capture, platform, disease stage and control source as the source gives them, the stage of each sample in the atlas, and donors / samples / cells deposited and in the atlas |
| [`table1_footnotes.md`](table1_footnotes.md) | what the columns count, and study-by-study notes on what is included and why |

| | studies | donors | samples | cells |
|---|---:|---:|---:|---:|
| deposited (in scope) | 28 | 356 | 433 | 2,186,795 |
| in the atlas (Figure 1) | 28 | 337 | 405 | 1,855,148 |

The `Dataset` column is the study name used everywhere in the code, and `01_download/download_manifest.csv` uses it
as well.
