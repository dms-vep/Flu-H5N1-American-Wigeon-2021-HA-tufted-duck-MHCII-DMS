# H5N1 American Wigeon 2021 HA-MHCII Binding DMS - Analysis Notebooks

This directory contains analysis notebooks for processing virus titer data, VLP neutralization curves, and other non-DMS data. Note that all experiments use either pseudovirus or conditionally replicative influenza virus for safety reasons. 

## Usage

All notebooks need to be run manually. Each folder contains its own README with specific instructions. 

## Folder Contents

### Analysis Overview

Each folder contains specialized analysis workflows for different aspects of influenza virus entry, binding, and neutralization studies. All experiments use pseudovirus or conditionally replicative viruses for safety.

| Folder | Purpose | Main Files | Outputs |
|--------|---------|------------|---------|
| **`chimeraX_outputs/`** | **Structural visualization**: Create ChimeraX B-factor attribute files for mapping DMS effects onto 3D protein structures | `plot_binding.ipynb`, `plot_entry_difference.ipynb` | `*.defattr` files for ChimeraX |
| **`conditionally_replicative_h5_titers/`** | **Replicative virus titers**: Process and visualize titer measurements from conditionally replicative H5 influenza viruses | `plot_titers.ipynb` | `conditional_flu_virus_titers.html` |
| **`dms_entry_correlations/`** | **Correlation analysis**: Generate scatter plots showing correlations between pseudovirus entry titers across different cell lines with interactive features | `entry_black_dots.py`, `config.yaml` | `entry_correlation_plots.html` |
| **`entry_titer_comparison_between_MHCIIs/`** | **Multi-subtype comparison**: Compare influenza pseudovirus entry titers from different subtypes (H1, H3, H5) on various MHCII-expressing cell lines | `virus_titers.ipynb` | `virus_titers_by_strain.html`, `increase_over_noSA_by_strain.html`, `virus_titers.csv` |
| **`H1_H2_H3_MHCII_entry_titers/`** | **Historical subtype screening**: Analyze binding titers of H1, H2, and H3 influenza viruses to different MHCII cell lines using 96-well plate experiments | `plot_virus_titers.py` | Multiple HTML plots and CSV files |
| **`H5-HA-MHCII-binding-screen/`** | **H5 binding screen**: Comprehensive screening of H5 influenza hemagglutinin binding to various MHCII-expressing cell lines with quality control and fold-change analysis | `plot_virus_titers.py`, `virus_titers.ipynb` | Multiple HTML interactive plots and processed CSV files |
| **`H5_pseudovirus_entry_validations_on_different_cell_lines/`** | **Entry validation**: Validate pseudovirus entry measurements across different cell line variants with variant-specific analysis | `virus_titers.ipynb` | `virus_titers_by_variant.html`, `increase_over_noSA_by_variant.html` |
| **`H5_titers_in_sialic_acid_and_MHCII_expressing_cells/`** | **Dual receptor analysis**: Measure H5 virus titers on cell lines expressing both sialic acid receptors and MHCII molecules | `virus_titers.ipynb` | `virus_titers.html` |
| **`MHCII_protein_sequence_comparison/`** | **MHCII sequence identity analysis**: Calculate pairwise protein sequence identity between MHCII alpha and beta chains and generate compact heatmaps for publication | `mhcii_sequence_identity_heatmap.py` | `*.svg` heatmaps, `*.csv` identity matrices |
| **`MHCII_VLP_neutralization/`** | **VLP neutralization curves**: Fit Hill curves to VLP neutralization data and create interactive neutralization curve visualizations | `neuts_altair.ipynb` | `neutralization_curves.html`, `ICXX.csv` |
| **`MHCII_VLP_neutralization_DMS_validations/`** | **DMS neutralization validation**: Validate DMS findings using VLP neutralization assays with curve fitting and interactive plots | `neuts_altair_dms_validations.ipynb` | `neutralization_curves_dms_validations.html`, `ICXX_dms_validations.csv` |
| **`strain_titers_with_trees/`** | **Integrated phylogenetic analysis**: Combine virus titer data with phylogenetic tree visualizations to show evolutionary relationships | `plot_titers_w_trees.py` | Multiple files in `./results/` |

### Common Analysis Features

- **Interactive visualizations**: Most analyses generate HTML files with Altair/Vega-Lite interactive plots
- **Quality control**: Automated filtering of failed virus rescues and low-quality measurements
- **Error analysis**: Standard error calculations and propagation for replicate measurements
- **Hover tooltips**: Detailed information available on mouseover in interactive plots
- **Log-scale axes**: Appropriate scaling for wide-range titer data
- **Color coding**: Consistent color schemes for cell lines, virus types, and experimental conditions
