---
aside: false
---

# Titers of H5 HA-pseudotyped viruses on different cell lines

Here, we measure titers of pseudoviruses pseudotyped with H5 HAs from 80 different influenza strains on several cell lines:

* **noSA cells**: cells that do not express MHC-II or sialic acid.
* **noSA–tufted duck MHC-II cells**: cells that do not express sialic acid but express tufted duck MHC-II.
* **noSA–human MHC-II cells**: cells that do not express sialic acid but express human MHC-II with different MHC-II beta-chain alleles:

  * noSA–human-MHCII–15:03
  * noSA–human-MHCII–03:01
* **SA23 cells**: cells expressing only α2,3-linked sialic acids.

## Titers normalized to noSA cells

The interactive plot below shows pseudovirus titers normalized to titers on noSA cells. Viruses are arranged by phylogenetic clade.

You can display or hide specific cell lines by clicking the corresponding cells in the legend.

<Figure caption="H5 HA-pseudotyped lentivirus titers on different cell lines, normalized to noSA cells">
    <Altair :showShadow="true" :spec-url="'https://raw.githubusercontent.com/dms-vep/Flu-H5N1-American-Wigeon-2021-HA-tufted-duck-MHCII-DMS/refs/heads/master/analysis_notebooks/strain_titers_with_trees/charts/H5_titer-relative-to-noSA_horizontal.html'"></Altair>
</Figure>

## Raw titers

The plot below shows the same data as above but as raw titers measured on each cell line.

<Figure caption="Raw titers of H5 HA-pseudotyped lentiviruses on different cell lines">
    <Altair :showShadow="true" :spec-url="'https://raw.githubusercontent.com/dms-vep/Flu-H5N1-American-Wigeon-2021-HA-tufted-duck-MHCII-DMS/refs/heads/master/analysis_notebooks/strain_titers_with_trees/charts/H5_raw-titer_horizontal.html'"></Altair>
</Figure>
