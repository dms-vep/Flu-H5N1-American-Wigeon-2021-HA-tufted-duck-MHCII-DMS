---
aside: false
---

# Effects of H5 HA mutations on entry in cells expressing tufted duck MHC-II or sialic acid

This page shows how mutations to H5 HA affect its ability to mediate pseudovirus entry in cells expressing no sialic acid but tufted duck MHC-II, or in cells expressing sialic acid.

[[toc]]

## Differences in how mutations affect entry in various cells

Most HA mutations have similar effects on entry in cells expressing tufted duck MHC-II or sialic acid---however, mutations at key sites involved in interacting with MHC-II or sialic acid have different effects in different target cells.

The interactive plot below shows how each HA mutation affects entry into:
 - a mix of cells expressing a2-3-linked (SA23) and a2-6-linked (SA26) sialic acids
 - cells expressing no sialic acid but tufted duck MHC-II
 - cells expressing only a2-3-linked sialic acids (SA23)
 - cells expressing only a2-6-linked sialic acids (SA26)

The line plot shows the total difference in effects of mutations at each site (using [H3 numbering](numbering)) on a pair of cells (use the dropdown at the bottom to choose the two cell lines that are compared).
Sites with large positive or negative values have mutations that are more favorable for entry in one cell than another.

Clicking on a site in the line plot makes the scatter plot to the right display the mutation-level effects for that site in the two cell lines.
It also makes the heat maps at bottom show the effects of all mutations at that site (and neighboring sites) on entry in all cell lines. 
In the heat maps, red shades indicates a mutation impairs entry, blue indicates a mutation enhances on entry, grey indicates no mutationwas made for a mutation, and `x` indicates the wildtype amino acid in the A/American Wigeon/South Carolina/USDA-000345-001/2021 (H5N1) HA.

Click on the box in the upper right of the below plot to expand it to full page.

<Figure caption="Effects of mutations in H5 HA on different cell lines">
    <Altair :showShadow="true" :spec-url="'htmls/compare_cell_entry_site_zoom.html'"></Altair>
</Figure>

Additional relevant links:

 - [standalone link to the heatmaps shown above](htmls/compare_cell_entry_site_zoom.html){target="_self"}
 - [heatmap showing effects of all mutations on all cell lines](htmls/entry_all_cells_overlaid.html){target="_self"}
 - [comparable plots for a H7 rather than H5 HA](https://dms-vep.org/Flu-H7-Anhui13-MHCII-binding/)

## HA structure colored by mutation effects on entry in MHC-II versus sialic acid expressing cells
Below is the H5 HA structure showing the sites where mutations have different effects on entry in sialic-acid versus tufted duck MHC-II expressing cells on H5 HA structure.
Red indicates sites where mutations are more deleterious for entry in  MHC-II expressing cells, and blue indicates sites where mutations are more deleterious for entry in sialic-acid expressing cells.

<video autoplay muted loop playsinline width="100%" style="display: block;">
  <source src="./difference_H5.mp4" type="video/mp4">
</video>

See the plot below to explore the data in an interactive structural context using [dms-viz](https://dms-viz.github.io/dms-viz-docs/).
Click on a site in the line plot of differences in entry between the cells to highlight the site on the structure, or to color all sites click on the *Select All Sites* option.
[Use this link](https://dms-viz.github.io/v0/?data=https%3A%2F%2Fraw.githubusercontent.com%2Fdms-vep%2FFlu-H5N1-American-Wigeon-2021-HA-tufted-duck-MHCII-DMS%2Frefs%2Fheads%2Fmaster%2Fresults%2Fdms-viz%2Fcell_entry_diffs_on_4kwm%2Fcell_entry_diffs_on_4kwm.json) for a standalone version of the interactive plot below. 

<iframe src="https://dms-viz.github.io/v0/?data=https%3A%2F%2Fraw.githubusercontent.com%2Fdms-vep%2FFlu-H5N1-American-Wigeon-2021-HA-tufted-duck-MHCII-DMS%2Frefs%2Fheads%2Fmaster%2Fresults%2Fdms-viz%2Fcell_entry_diffs_on_4kwm%2Fcell_entry_diffs_on_4kwm.json" width="100%" height="700px"></iframe>

## Numerical values of mutations effects on cell entry
For numerical data, see the following CSVs; note that *site* refers to [H3 numbering](numbering):
 - [Effects of each mutation on entry in each cell line, after recommended QC](https://github.com/dms-vep/Flu-H5N1-American-Wigeon-2021-HA-MHCII-DMS/blob/main/results/summaries/entry_all_cells.csv)
 - [Differences in mutation effects on entry in each cell line, after applying the QC and effect floors / ceilings used in plots above](https://github.com/dms-vep/Flu-H5N1-American-Wigeon-2021-HA-MHCII-DMS/blob/main/results/compare_cell_entry/mut_diffs.csv)
 - See links in the *Functional effects of mutations* subsection of the [Appendix](appendix.html){target="_self"} to see additional CSV files with mutation effects without the various QC filters applied above.
