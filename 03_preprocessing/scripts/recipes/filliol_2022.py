"""filliol_2022 (GEO GSE174748): Seurat object of the human liver nuclei (GSE174748_hl_nuclei.rds.gz) with the authors'
per-cell metadata; counts from the RNA assay, read through R (readers.from_seurat).
source_sample_id = the GEO sample (GSM) of each library (orig.ident)."""
from readers import from_seurat

ACC = 'GSE174748'
GSM = {'Healthy1': 'GSM5325534', 'Healthy2': 'GSM5325535', 'NAFLD1': 'GSM5325536', 'NAFLD2': 'GSM5325537'}


def build(raw):
    a = from_seurat(raw / ACC / f'{ACC}_hl_nuclei.rds.gz')
    a.obs['source_sample_id'] = a.obs['orig.ident'].map(GSM)
    assert a.obs.source_sample_id.notna().all(), 'library without a GSM'
    return a
