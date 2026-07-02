---
aside: false
---

# Tufted duck MHC-II VLP binding

Here we measure the effect of mutations in H5 HA on binding to tufted duck MHC-II virus-like particles (MHCII-VLPs). For these experiments MHCII-VLPs were produced by co-transfecting lentiviral Gag protein with tufted duck MHC-II expression plasmid into cells, which leads to production of Gag-formed VLPs coated with MHC-II. We can then use these MHCII-VLPs to neutralize our H5 HA pseudovirus-based deep mutational scanning libraries and identify mutations that affect MHCII-VLP binding. Note that because produced MHCII-VLPs contain more than just a soluble MHC-II protein (e.g. they include other cell membrane proteins) in these experiments we map effects of mutations on binding to VLP itself not just MHC-II. For example, we are also mapping effects of mutations on binding to sialylated proteins that might normally be expressed on cell membranes from which the VLPs are made. 

## Interactive heat map of effects of mutations on tufted duck MHCII-VLP binding

In the interactive chart below shows the total effects of mutations at each site in HA, and the heat map shows the effects of individual mutations. Note that the two different shades of gray in the heat maps have differing meanings: light gray means a mutation was missing (not measured) in the library, whereas dark gray means a mutation was measured but was so deleterious for cell entry it is not possible to reliably estimate its effect on other phenotypes (the threshold for how deleterious a mutation must be for cell entry to be shown in dark gray is controlled by the cell entry slider at the bottom of the plot).


<Figure caption="Effects of mutations in H5 HA on tufted duck MHCII-VLP binding">
    <Altair :showShadow="true" :spec-url="'htmls/tufted_duck_MHCII_binding_mut_effect.html'"></Altair>
</Figure>

Numerical data for mutation effects on binding is available[here](https://github.com/dms-vep/Flu-H5N1-American-Wigeon-2021-HA-tufted-duck-MHCII-DMS/blob/master/results/summaries/tufted_duck_MHCII_binding.csv) 


Below is structure generated using [ChimeraX](https://www.cgl.ucsf.edu/chimerax/) showing MHCII-VLP binding data on H5 HA structure. Red indicates sites were most mutations decrease MHCII-VLP binding and blue indicates sites were most mutations increase MHCII-VLP binding

<video autoplay muted loop playsinline width="100%" style="display: block;">
  <source src="./binding_H5.mp4" type="video/mp4">
</video>

