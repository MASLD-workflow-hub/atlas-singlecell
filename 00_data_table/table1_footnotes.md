# Footnotes to Table 1

## Columns

1. **Deposited** (`Donors / Samples / Cells deposited`): the human 10x Genomics libraries of each deposit that are in scope:
   control or MASLD tissue, one source per study, and each person in one study only. Samples are sequencing libraries.
   Totals: 356 donors, 433 samples, 2,186,795 cells.
2. **In atlas** (`Donors / Samples / Cells in atlas`): the cells of the integrated atlas shown in Figure 1 after quality
   control, a clinical review of every sample, and cell-type annotation: 337 donors, 405 samples, 1,855,148 cells.
   `Cells deposited, atlas samples` counts the deposited cells of those 405 samples (2,068,160). Cells that did not reach
   the atlas (low quality, doublets, ambient-dominated, no lineage signal) are kept in sidecar tables with the reason.
3. **Disease stage (source wording)** is the diagnosis supported by the metadata, followed in brackets by the deposit's own
   wording, verbatim ('Boderline NASH [sic]' is the depositors' spelling). The source diagnosis is never changed.
4. **Disease stage in the atlas (samples)** is the stage each atlas sample is analysed under, after a hepatologist reviewed
   every sample (Control, MASL, MASLD unstaged, Borderline MASH, MASH, Cirrhosis). The figures use five clinical groups
   and count Borderline MASH as MASH.
5. **Control source** says why the control tissue was taken. A bracket applies the MASLD definition (steatosis plus a
   cardiometabolic risk factor) as a flag: the authors' control label is kept, and flagged controls are not used as a
   healthy reference.

## Studies

6. andrews_2022: the libraries of donors C41, C58 and C70 are counted here and not under andrews_2024 (same people).
7. andrews_2024: donor C59 is not included (recorded sex contradicts expression).
8. buonomo_2022: control livers only; the cirrhotic livers of unstated cause are not included. 5 of the 13 control
   libraries (donors P1, P2, P5) have recorded steatosis and are flagged.
9. dominguezconde_2022: the liver object of this cross-tissue study holds immune cells only.
10. dong_2024: 'mild' comes from the GEO series summary; the per-sample field reads 'NAFLD'. Controls are biopsies of
    deceased-donor livers procured for transplantation.
11. gribben_2024: control donor P98 (screening biopsy, steatosis S1, BMI 33.9) meets the MASLD definition and is flagged.
    The end-stage arm has no per-sample aetiology; the GEO series design states 'end-stage disease due to NAFLD
    progression'. Patient 6 (deposit and supplement disagree on the diagnosis) and P56 (sex mismatch) are not included.
12. guilliams_2022: the authors present all donors as one healthy-liver cohort. The 9 donors with recorded steatosis of
    5 % or more each have a cardiometabolic risk factor in the paper's clinical table and are flagged as meeting the MASLD
    definition. Donor H21 (hepatocellular carcinoma) is not included.
13. henderson_unpublished: an unpublished Henderson lab (Edinburgh) cohort, taken from the Human Liver Cell Atlas (HLiCA)
    release: sorted endothelial and mesenchymal cells of 16 resection donors. No library duplicates a library of
    ramachandran_2019, filliol_2022 or papachristoforou_2025 (barcode check).
14. hong_2025: controls have steatosis < 5 % and fibrosis stage 0; MASL donors stage 0; advanced MASH donors stage 3
    (no cirrhosis). Author cell labels come from the authors' object on Zenodo (10.5281/zenodo.14586466).
15. jimenez-gracia_2026: blood (white blood cells) of two MASH cirrhosis patients. They share two pooled libraries with
    alcohol-cirrhosis patients; cells are assigned to patients with the authors' object on Zenodo
    (10.5281/zenodo.14851901), matched by library and barcode. Cells of other patients or without an assignment are not
    included.
16. jones_2022 (Tabula Sapiens): the consortium's CELLxGENE liver file; Smart-seq2 cells are not included. Part of the
    cells come from the Tabula Sapiens 2.0 release (bioRxiv 2024, doi 10.1101/2024.12.03.626516). Donor TSP14 has a
    recorded history of alcohol abuse, hypertension and coronary artery disease and is flagged.
17. kim_2025: nuclei from snap-frozen whole liver. Donors JB321 and JB337 (GEO and the supplement swap their MASL and MASH
    labels) and JB289 (sex mismatch) are not included. Chemistry (3' v3.1) is from the supplementary methods.
18. maretti-mira_2023: cirrhosis is stated in the series design; the per-sample field reads 'NASH'. The HCV and PSC
    explants are not included.
19. ramachandran_2019: 5 healthy livers, 2 NAFLD-cirrhotic livers and blood of 3 donors with NAFLD cirrhosis. Whether the
    blood donors are also liver donors is not stated, so the number of people is between 7 and 10.
20. steixner-kumar_2025: one deposit term ('MAFLD/MASH') for all patients; white blood cells, not PBMC.
21. sugimoto_2025: control S28 is female by the supplementary table and expression (the GEO field says male). The
    alcohol-associated samples are not included. Supplementary Table 10 gives the control source only as 'Deceased donor'.
22. wang_2023: donor NASH_6 is not included (sex mismatch). Author cell labels come from the authors' processed object
    on GEO.
23. watson_2025: control donors from GEO GSE210077. Not included: three fibrotic livers of unstated cause; Liver-4 and
    Liver-6 (their data are swapped between GEO and the HLiCA release); Liver-21 (its GEO slot holds a copy of Liver-2).
    The healthy group may include grade 1 steatosis (no per-donor grade published), so no sample is flagged individually.
24. xiao_2023: the three 'healthy' livers are from deceased donors; histology and BMI are not reported for them. No NAS
    or fibrosis stage is published for the three NASH donors. Chemistry (3' v3.1) is from the supplementary materials.
25. yakubovsky_2026: the paper reports 4 donors; donor M8 is not included (sex mismatch).
