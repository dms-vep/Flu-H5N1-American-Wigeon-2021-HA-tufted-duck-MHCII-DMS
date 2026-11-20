---
aside: false
---

# Nextstrain phylogenetic trees of HA annotated by MHC-II interactions
We have created interactive Nextstrain trees of HA from key subtypes to help view the data about MHC-II usage in an evolutionary context.

The trees can be colored by:
 - the amino-acid identity at different HA sites
 - the host species for that viral strain
 - for strains with directly measured [entry titers](entry_titers), those titers measured on different cells
 - predicted tufted duck MHC-II usage as determined by summing or taking the max of the effects of all mutations as measured in the deep mutational scanning (these predictions assume mutations are non-epistatic and have the same effects across strains, which is increasingly untrue asstrains become more distant from the specific H5 and H7 strains used in the deep mutational scanning)

[[toc]]

## Examples of how to view HA trees (for H5 HA)
Here we show some examples of how to view the H5 HA trees.

For each subtype, we make several trees:
 - a tree with just the strains for which we directly measures MHC-II or sialic-acid [entry titers](entry_titers)
 - a compact tree with a broad set of HAs subsampled to just a few hundred sequences
 - a larger tree with a broad set of HAs subsampled to a few thousand sequences (when that many are available)

Each tree can be colored by different properties using the *Color By* dropdown, specifically:
 - The amino-acid identity at different HA sites (using the *Genotype* option); note that the subtype-specific *SigPep* / *HA1* / *HA2* numbering scheme used for the sites **differs from the H3 numbering scheme used on the rest of this site**; see the subtype-specific numbering TSVs (eg, [here for H5](https://github.com/jbloomlab/flu-ha-mhcii-usage-trees/blob/master/data/trees/H1/protein_sites.tsv)) to interconvert.
 - The host species for that viral strain (using *host general* or *host order*).
 - For strains with directly measured pseudovirus [entry titers](entry_titers), those titers measured on different cells. For instance, *log10_293-noSA-tufted-duck-MHCII_over_293-noSA_titers* indicates the titer on the tufted duck MHC-II cells relative to the no-sialic acid cells.
 - Predicted tufted duck MHC-II usage as determined by summing or taking the max of the effects of all mutations as measured in the deep mutational scanning (these predictions assume mutations are non-epistatic and have the same effects across strains, which is increasingly untrue as strains become more distant from the specific H5 and H7 strains used in the deep mutational scanning). For instance, *MHCII entry increase (H5), total effect* is the summed effects of mutations on MHC-II mediated entry.

For instance, below is a view of the H5 HA tree of just strains for which we measured the titers, colored by the host species (click [here](https://nextstrain.org/community/jbloomlab/flu-ha-mhcii-usage-trees/H5-with-titers) for a standalone link):
<iframe src="https://nextstrain.org/community/jbloomlab/flu-ha-mhcii-usage-trees/H5-with-titers" width="100%" height="700px"></iframe>

Here is the same tree but colored by the measured entry titers on tufted duck MHC-II cells relative to the noSA cells (click [here](https://nextstrain.org/community/jbloomlab/flu-ha-mhcii-usage-trees/H5-with-titers?c=log10_293-noSA-tufted-duck-MHCII_over_293-noSA_titer) for a stanalone link):
<iframe src="https://nextstrain.org/community/jbloomlab/flu-ha-mhcii-usage-trees/H5-with-titers?c=log10_293-noSA-tufted-duck-MHCII_over_293-noSA_titer" width="100%" height="700px"></iframe>

In all of these trees, you can mouse over tip nodes for details, etc.

There are also other interactive display options; for instance here are the data displayed as a scatter plot of the directly measured tufted duck MHC-II entry titers versus the amino acid identity at site *HA1 71* (H3 site 80, see [here](https://github.com/jbloomlab/flu-ha-mhcii-usage-trees/blob/master/data/trees/H5/protein_sites.tsv)); this shows that the strains with very low tufted duck MHC-II entry mostly have a mutation of this site to T (click [here](https://nextstrain.org/community/jbloomlab/flu-ha-mhcii-usage-trees/H5-with-titers?c=gt-HA1_71&l=scatter&scatterX=gt&scatterY=log10_293-noSA-tufted-duck-MHCII_over_293-noSA_titer) for a standalone link):
<iframe src="https://nextstrain.org/community/jbloomlab/flu-ha-mhcii-usage-trees/H5-with-titers?c=gt-HA1_71&l=scatter&scatterX=gt&scatterY=log10_293-noSA-tufted-duck-MHCII_over_293-noSA_titer" width="100%" height="700px"></iframe>

## Links to trees for all HA subtypes

A list of all the Nextstrain interactive trees is at [https://nextstrain.org/community/jbloomlab/flu-ha-mhcii-usage-trees](https://nextstrain.org/community/jbloomlab/flu-ha-mhcii-usage-trees).
Below are links to the specific trees for each subtype, as well as links to files mapping the H3 numbering scheme used for all other plots on this site to the subtype-specific *SigPep* / *HA1* / *HA2* numbering scheme used by the trees:

- H1 HAs:
  + [HAs with directly measured pseudovirus entry titers](https://nextstrain.org/community/jbloomlab/flu-ha-mhcii-usage-trees/H1-with-titers)
  + [HAs, compact sequence set](https://nextstrain.org/community/jbloomlab/flu-ha-mhcii-usage-trees/H1-compact)
  + [HAs, larger sequence set](https://nextstrain.org/community/jbloomlab/flu-ha-mhcii-usage-trees/H1)
  + [File mapping the site labels used for the Nextstrain trees (*protein*, *protein_site*) to H3 numbering (*H3_site*) and other numbering schemes](https://github.com/jbloomlab/flu-ha-mhcii-usage-trees/blob/master/data/trees/H1/protein_sites.tsv)
- H2 HAs:
  + [HAs with directly measured pseudovirus entry titers](https://nextstrain.org/community/jbloomlab/flu-ha-mhcii-usage-trees/H2-with-titers)
  + [HAs, compact sequence set](https://nextstrain.org/community/jbloomlab/flu-ha-mhcii-usage-trees/H2-compact)
  + [HAs, larger sequence set](https://nextstrain.org/community/jbloomlab/flu-ha-mhcii-usage-trees/H2)
  + [File mapping the site labels used for the Nextstrain trees (*protein*, *protein_site*) to H3 numbering (*H3_site*) and other numbering schemes](https://github.com/jbloomlab/flu-ha-mhcii-usage-trees/blob/master/data/trees/H2/protein_sites.tsv)
- H3 HAs:
  + [HAs with directly measured pseudovirus entry titers](https://nextstrain.org/community/jbloomlab/flu-ha-mhcii-usage-trees/H3-with-titers)
  + [HAs, compact sequence set](https://nextstrain.org/community/jbloomlab/flu-ha-mhcii-usage-trees/H3-compact)
  + [HAs, larger sequence set](https://nextstrain.org/community/jbloomlab/flu-ha-mhcii-usage-trees/H3)
  + [File mapping the site labels used for the Nextstrain trees (*protein*, *protein_site*) to H3 numbering (*H3_site*) and other numbering schemes](https://github.com/jbloomlab/flu-ha-mhcii-usage-trees/blob/master/data/trees/H3/protein_sites.tsv)
- H5 HAs:
  + [HAs with directly measured pseudovirus entry titers](https://nextstrain.org/community/jbloomlab/flu-ha-mhcii-usage-trees/H5-with-titers)
  + [HAs, compact sequence set](https://nextstrain.org/community/jbloomlab/flu-ha-mhcii-usage-trees/H5-compact)
  + [HAs, larger sequence set](https://nextstrain.org/community/jbloomlab/flu-ha-mhcii-usage-trees/H5)
  + [File mapping the site labels used for the Nextstrain trees (*protein*, *protein_site*) to H3 numbering (*H3_site*) and other numbering schemes](https://github.com/jbloomlab/flu-ha-mhcii-usage-trees/blob/master/data/trees/H5/protein_sites.tsv)
- H7 HAs:
  + [HAs, compact sequence set](https://nextstrain.org/community/jbloomlab/flu-ha-mhcii-usage-trees/H7-compact)
  + [HAs, larger sequence set](https://nextstrain.org/community/jbloomlab/flu-ha-mhcii-usage-trees/H7)
  + [File mapping the site labels used for the Nextstrain trees (*protein*, *protein_site*) to H3 numbering (*H3_site*) and other numbering schemes](https://github.com/jbloomlab/flu-ha-mhcii-usage-trees/blob/master/data/trees/H7/protein_sites.tsv)

## Source code and underlying Auspice JSONs for the trees
The trees above are generated by the GitHub repository [https://github.com/jbloomlab/flu-ha-mhcii-usage-trees](https://github.com/jbloomlab/flu-ha-mhcii-usage-trees), which contains methods details and all the code.

The Auspice JSONs for the trees themselves are [here](https://github.com/jbloomlab/flu-ha-mhcii-usage-trees/tree/master/auspice) and are rendered as [Nextstrain Community Builds](https://docs.nextstrain.org/en/latest/guides/share/community-builds.html) at the links above.
