---
aside: false
---

# Effects of H5 HA mutations on binding to tufted duck MHC-II VLPs

This page shows how mutations to H5 HA affect binding to tufted duck MHC-II virus-like particles (VLPs), as assessed by the ability of these VLPs to neutralize pseudovirus infectivity.
Note that because the MHC-II VLPs may also contain other cell membrane proteins, some of the HA mutations may also affect binding to this proteins as well as MHC-II.

[[toc]]

## Heatmap of how mutations affect tufted duck MHCII-VLP binding

In the interactive chart below, the line plot shows the total effects of mutations at each site in HA on MHC-II VLP binding, and the heatmap shows the effects of individual mutations.

The heatmap shows the effects of individual mutations: positive values (blue) indicate mutations increase binding (as assessed by increased MHC-II VLP neutralization of pseudovirus) and negative values (orange) indicate mutations decrease binding.
Light gray in the heatmap means a mutation was not measured, and dark gray means the mutation wsa so deleterious for HA-mediated cell entry that it was not possible to reliably estimate its effect on MHC-II binding.
The `x` for each site indicates the wildtype amino acid in the A/American Wigeon/South Carolina/USDA-000345-001/2021 (H5N1) HA.
Mouse over mutations on the heatmap for details.

Below the chart are interactive options to adjust parameters on the chart.
Click the box in the upper right to expand the chart to full page.

<Figure caption="Effects of mutations in H5 HA on tufted duck MHCII-VLP binding">
    <Altair :showShadow="true" :spec-url="'htmls/tufted_duck_MHCII_binding_mut_effect.html'"></Altair>
</Figure>

Additional relevant links:

 - [standalone link to the chart shown above](htmls/tufted_duck_MHCII_binding_mut_effect.html){target="_self"}
 - [chart showing effects of mutations on MHC-II binding alongside the effects on cell entry](htmls/tufted_duck_MHCII_binding_overlaid.html){target="_self"}

## HA structure colored by mutation effects on MHC-II binding

Below is structure of H5 HA colored by the total effect of all mutations at each site on tufted duck MHC-II VLP binding.
Red indicates sites where most mutations decrease MHCII-VLP binding and blue indicates sites where most mutations increase MHCII-VLP binding

<video autoplay muted loop playsinline width="100%" style="display: block;">
  <source src="./binding_H5.mp4" type="video/mp4">
</video>

## Numerical values of mutation effects on MHC-II binding
For numerical data, see the following CSVs; note that *site* refers to [H3 numbering](numbering):
  - [Effects of mutations on MHC-II binding after recommended QC](https://github.com/dms-vep/Flu-H5N1-American-Wigeon-2021-HA-tufted-duck-MHCII-DMS/blob/master/results/summaries/tufted_duck_MHCII_binding.csv) 
  - [Measured effects on MHC-II binding with full QC details but QC not pre-applied to numerical values](https://github.com/dms-vep/Flu-H5N1-American-Wigeon-2021-HA-tufted-duck-MHCII-DMS/blob/master/results/MHCII_binding/averages/tufted_duck_MHCII_binding_mut_effect.csv) (only use this file if you understand QC filters)
