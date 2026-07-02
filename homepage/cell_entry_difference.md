---
aside: false
---

# Cell Entry difference

Here we measure the difference in effects of mutations in H5 HA on entry in cells expressing sialic acids (SA23, SA26 or SA23-SA26 cells in the drop down meniu) and cells expressing tufted duck MHCII (tufted duck MHCII cells).

Because only a small number of sites in HA are expected to directly mediate receptor binding, most mutations should have similar effects on entry regardless of the cell line used. However, mutations at sites involved in receptor binding are expected to have different effects depending on which receptor is expressed by the target cells.

This interactive plot summarizes, at each HA site, how mutations differentially affect cell entry between the selected cell types. In the line plot, each point corresponds to an HA site, shown using H3 numbering. The plotted value represents the average difference in mutational effects on entry between the two compared cell types. Sites with values near zero have similar mutation effects in both entry conditions, whereas sites with large positive or negative values identify regions where mutations preferentially affect entry in one cell type relative to the other.

Clicking on any point in the line plot displays the mutation-level effects for that site in the scatter plot on the right, showing how individual mutations compare between the two selected cell lines. You can also zoom in on a specific region of the line plot, and the heat maps below will show mutation-level effects across all cell lines for the selected region.

In the heat maps, red shades indicate deleterious effects on entry, and blue shades indicate beneficial effects on entry. Light grey squares indicate mutations without measurements. An “x” indicates the wild-type amino acid in the A/American Wigeon/South Carolina/USDA-000345-001/2021 (H5N1) HA sequence.

<Figure caption="Effects of mutations in H5 HA on different cell lines">
    <Altair :showShadow="true" :spec-url="'htmls/compare_cell_entry_site_zoom.html'"></Altair>
</Figure>

Numerical data for mutation effects on entry in different cell lines can be found [here](https://github.com/dms-vep/Flu-H5N1-American-Wigeon-2021-HA-tufted-duck-MHCII-DMS/blob/master/results/summaries/tufted_duck_MHCII_binding.csv) 


Below is structure generated using ChimeraX showing the entry difference data between SA23 and tufted duck MHC-II expressing cells on H5 HA structure. Red indicates sites that are more deletarious for entry in tufted duck MHC-II expressing cells and light blue are sites that are more deletarious for entry in SA23 cells.

<video autoplay muted loop playsinline width="100%" style="display: block;">
  <source src="./difference_H5.mp4" type="video/mp4">
</video>


To explore data in a structural context interactively use visualizations below made using the [dms-viz](https://dms-viz.github.io/dms-viz-docs/) platform. To see entry difference data overlaid on the HA, highlight some or all sites on the line plot above the structure. For a better visual under Protein Options on the left set ‘protein representation’ to cartoon and ‘selection representation’ to surface.


Click [here](https://dms-viz.github.io/v0/?data=https%3A%2F%2Fraw.githubusercontent.com%2Fdms-vep%2FFlu-H5N1-American-Wigeon-2021-HA-tufted-duck-MHCII-DMS%2Frefs%2Fheads%2Fmaster%2Fresults%2Fdms-viz%2Fcell_entry_diffs_on_4kwm%2Fcell_entry_diffs_on_4kwm.json) for a standalone version of the below plot. 

<iframe src="https://dms-viz.github.io/v0/?data=https%3A%2F%2Fraw.githubusercontent.com%2Fdms-vep%2FFlu-H5N1-American-Wigeon-2021-HA-tufted-duck-MHCII-DMS%2Frefs%2Fheads%2Fmaster%2Fresults%2Fdms-viz%2Fcell_entry_diffs_on_4kwm%2Fcell_entry_diffs_on_4kwm.json" width="100%" height="500px"></iframe>