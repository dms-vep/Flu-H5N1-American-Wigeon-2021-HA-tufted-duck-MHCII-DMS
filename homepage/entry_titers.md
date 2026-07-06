---
aside: false
---

# Titers of HA-pseudotyped viruses on different cell lines

We measured titers of pseudoviruses pseudotyped with HAs from different influenza subtypes and strains on several cell lines:

* **noSA cells**: cells that do not express MHC-II or sialic acid.
* **noSA–tufted duck MHC-II cells**: cells that do not express sialic acid but express tufted duck MHC-II.
* **noSA–human MHC-II cells**: cells that do not express sialic acid but express human MHC-II with different MHC-II beta-chain alleles:

  * noSA–human-MHCII–15:03
  * noSA–human-MHCII–03:01
* **SA23 cells**: cells expressing only α2,3-linked sialic acids.
* **SA26 cells**: cells expressing only α2,6-linked sialic acids.

## Titers of H5 HA-pseudotyped viruses

Here, we measure titers of pseudoviruses pseudotyped with H5 HAs from 80 different influenza strains on different cell lines.

The interactive plot below shows pseudovirus titers normalized to titers on noSA cells. Viruses are arranged by phylogenetic clade.

You can display or hide specific cell lines by clicking the corresponding cells in the legend.

<Figure caption="H5 HA-pseudotyped lentivirus titers on different cell lines, normalized to noSA cells">
    <Altair :showShadow="true" :spec-url="'https://raw.githubusercontent.com/dms-vep/Flu-H5N1-American-Wigeon-2021-HA-tufted-duck-MHCII-DMS/refs/heads/master/analysis_notebooks/strain_titers_with_trees/charts/H5_titer-relative-to-noSA_horizontal.html'"></Altair>
</Figure>

The plot below shows the same data as above but as raw titers measured on each cell line.

<Figure caption="Raw titers of H5 HA-pseudotyped lentiviruses on different cell lines">
    <Altair :showShadow="true" :spec-url="'https://raw.githubusercontent.com/dms-vep/Flu-H5N1-American-Wigeon-2021-HA-tufted-duck-MHCII-DMS/refs/heads/master/analysis_notebooks/strain_titers_with_trees/charts/H5_raw-titer_horizontal.html'"></Altair>
</Figure>

## Titers of H1, H2 and H3 HA-pseudotyped viruses

Here, we measure titers of pseudoviruses pseudotyped with HAs from H1, H2 and H3 influenza strains on different cell lines.

The interactive plot below shows pseudovirus titers normalized to titers on noSA cells. Viruses are arranged by phylogenetic clade.

<Figure caption="H1 HA-pseudotyped lentivirus titers on different cell lines, normalized to noSA cells">
    <Altair :showShadow="true" :spec-url="'https://raw.githubusercontent.com/dms-vep/Flu-H5N1-American-Wigeon-2021-HA-tufted-duck-MHCII-DMS/refs/heads/master/analysis_notebooks/strain_titers_with_trees/charts/H1_titer-relative-to-noSA_vertical.html'"></Altair>
</Figure>
<Figure caption="H2 HA-pseudotyped lentivirus titers on different cell lines, normalized to noSA cells">
    <Altair :showShadow="true" :spec-url="'https://raw.githubusercontent.com/dms-vep/Flu-H5N1-American-Wigeon-2021-HA-tufted-duck-MHCII-DMS/refs/heads/master/analysis_notebooks/strain_titers_with_trees/charts/H3_titer-relative-to-noSA_vertical.html'"></Altair>
</Figure>
<Figure caption="H3 HA-pseudotyped lentivirus titers on different cell lines, normalized to noSA cells">
    <Altair :showShadow="true" :spec-url="'https://raw.githubusercontent.com/dms-vep/Flu-H5N1-American-Wigeon-2021-HA-tufted-duck-MHCII-DMS/refs/heads/master/analysis_notebooks/strain_titers_with_trees/charts/H3_titer-relative-to-noSA_vertical.html'"></Altair>
</Figure>

The plots below shows the same data as above but as raw titers measured on each cell line.

<Figure caption="H1 HA-pseudotyped lentivirus titers on different cell lines">
    <Altair :showShadow="true" :spec-url="'https://raw.githubusercontent.com/dms-vep/Flu-H5N1-American-Wigeon-2021-HA-tufted-duck-MHCII-DMS/refs/heads/master/analysis_notebooks/strain_titers_with_trees/charts/H1_raw-titer_vertical.html'"></Altair>
</Figure>
<Figure caption="H2 HA-pseudotyped lentivirus titers on different cell lines">
    <Altair :showShadow="true" :spec-url="'https://raw.githubusercontent.com/dms-vep/Flu-H5N1-American-Wigeon-2021-HA-tufted-duck-MHCII-DMS/refs/heads/master/analysis_notebooks/strain_titers_with_trees/charts/H1_raw-titer_vertical.html'"></Altair>
</Figure>
<Figure caption="H3 HA-pseudotyped lentivirus titers on different cell lines">
    <Altair :showShadow="true" :spec-url="'https://raw.githubusercontent.com/dms-vep/Flu-H5N1-American-Wigeon-2021-HA-tufted-duck-MHCII-DMS/refs/heads/master/analysis_notebooks/strain_titers_with_trees/charts/H1_raw-titer_vertical.html'"></Altair>
</Figure>

## Numerical pseudovirus entry titer data
For numerical raw and normalized titer data, see the following CSVs:
  - [H5 HA pseudovirus titer summary data](https://github.com/dms-vep/Flu-H5N1-American-Wigeon-2021-HA-tufted-duck-MHCII-DMS/blob/master/analysis_notebooks/H5-HA-MHCII-binding-screen/results/H5_pseudovirus_titer_summary.csv) 
  - [H1, H2 and H3 HA pseudovirus titer summary data](https://github.com/dms-vep/Flu-H5N1-American-Wigeon-2021-HA-tufted-duck-MHCII-DMS/blob/master/analysis_notebooks/H1_H2_H3_MHCII_entry_titers/results/pseudovirus_titer_summary.csv) 