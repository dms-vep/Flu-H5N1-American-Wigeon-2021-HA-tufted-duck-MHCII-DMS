---
layout: home

hero:
  name: Effects of mutations to an H5 HA on its interaction with tufted duck MHC-II
  tagline: Pseudovirus deep mutational scanning of how mutations to HA from A/American Wigeon/South Carolina/USDA-000345-001/2021 (H5N1) affects its interaction with tufted duck MHC-II
  image: logo.png
features:
  - title: Entry in MHC-II vs sialic-acid expressing cells
    details: Effects of H5 HA mutations on entry in cells expressing tufted duck MHC-II or sialic acid
    link: /entry
  - title: Binding to MHC-II
    details: Effects of H5 HA mutations on binding to tufted duck MHC-II VLPs
    link: /MHCII_binding_H5
  - title: Structural model of HA bound to MHC-II
    details: Cryo-EM based model of H5 HA bound to tufted duck MHC-II
    link: /H5_MHCII_structure
  - title: Effects of H7 HA mutations on MHC-II interaction
    details: Deep mutational scanning of how a H7 HA interacts with tufted duck MHC-II
    link: https://dms-vep.org/Flu-H7-Anhui13-MHCII-binding/
  - title: Effects of MHC-II mutations on interaction with HA
    details: Deep mutational scanning of how mutations to tufted duck MHC-II affect its interaction with a H5 HA
    link: https://dms-vep.org/Tufted-duck-MHCII-DMS/
  - title: HA trees annotated by MHC-II interactions
    details: Nextstrain phylogenetic trees of different HA subtypes annotated by MHC-II binding
    link: trees
  - title: HA sequence numbering
    details: Explanation of the HA sequence numbering scheme used here
    link: /numbering
---

## Overview

This website provides interactive visualizations and links to numerical data from pseudovirus deep mutational scanning measuring how mutations to an H5 HA (from A/American Wigeon/South Carolina/USDA-000345-001/2021) affect its interaction with tufted duck MHC-II.

For details about the study, see [Dadonaite et al. (2026)]() [**ADD CITATION**].

Visualizations and data can be accessed by clicking the gray boxes above for each type of measurement, namely:
 - [Effects of H5 HA mutations on entry in cells expressing tufted duck MHC-II or sialic acid](cell_entry_difference)
 - [Effects of H5 HA mutations on binding to tufted duck MHC-II](MHCII_binding_H5)
 - [Structural model of H5 HA bound to tufted duck MHC-II](H5_MHCII_structure)
 - [Effects of mutations to a H7 HA on interaction with MHC-II](https://dms-vep.org/Flu-H7-Anhui13-MHCII-binding/)
 - [Effects of mutations to tufted duck MHC-II on its interaction with H5 HA](https://dms-vep.org/Tufted-duck-MHCII-DMS/)
 - [Nextstrain phylogenetic trees of different HA subtypes annotated by MHC-II binding](trees)
 - [Explanation of the H3 HA numbering scheme used in plots shown here](numbering)

For numerical values of the effects of H5 HA mutations (H3 numbering) on interaction with MHC-II, see [this CSV](https://github.com/dms-vep/Flu-H5N1-American-Wigeon-2021-HA-tufted-duck-MHCII-DMS/blob/master/results/summaries/tufted_duck_MHCII_binding.csv).

For the full computer code and all numerical data files, see [the GitHub repository](https://github.com/dms-vep/Flu-H5N1-American-Wigeon-2021-HA-tufted-duck-MHCII-DMS).
For full documentation of the computational pipeline, see the [Appendix](appendix.html){target="_self"}.


## Biosafety
The experimental measurements were made using [pseudovirus deep mutational scanning](https://doi.org/10.1016/j.cell.2023.02.001) with [lentiviral particles pseudotyped](https://blog.addgene.org/viral-vectors-101-pseudotyping) with HA.
These pseudoviruses do not encode any viral proteins other than HA, and so are only able to undergo a single round of cell entry and are **not** fully replicative agents capable of spreading or causing disease.
They therefore provide a safe way to study mutations to the HA protein at biosafety-level-2 outside the context of actual pathogenic influenza.
The specific H5 HA pseudovirus deep mutational scanning libraries used for these experiments have [been previously described](https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.3002916).

See the biosafety statement in the paper about this study ([Dadonaite et al. (2026)]() [**ADD CITATION**]) for additional details.
