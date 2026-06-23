# DMS Entry Correlations Analysis

This folder contains analysis scripts for generating correlation plots between pseudovirus entry titers measured on different cell lines.

## Folder Structure

```
dms_entry_correlations/
├── config.yaml                    # Configuration file with data paths
├── entry_black_dots.py           # Main analysis script
├── entry_correlation_plots.html  # Interactive correlation plots (output)
└── README.md                     # This documentation
```

## Overview

The analysis creates interactive scatter plots showing pairwise correlations between pseudovirus entry measurements across four different cell lines:
- SA23 cells
- SA26 cells 
- SA23 SA26 mix cells
- tufted duck MHCII cells

## Input Data

- **Source**: Entry titer data specified in `config.yaml`
- **Path**: `../../results/summaries/entry_all_cells.csv`
- **Format**: CSV file containing entry measurements for different viral variants across multiple cell lines
- **Key columns**:
  - `site`: Position in the protein
  - `wildtype`: Original amino acid
  - `mutant`: Mutated amino acid
  - `entry in [cell line] cells`: Entry titer measurements for each cell line

## Output

- **File**: `entry_correlation_plots.html`
- **Format**: Interactive HTML file with embedded Altair/Vega-Lite visualizations
- **Content**: 6 correlation plots arranged in a 2×3 grid showing all pairwise comparisons

## Plot Features

- **Layout**: 2×3 grid of scatter plots (280×280 pixels each)
- **Data points**: Black circles with 30% opacity
- **Interactivity**: 
  - Hover tooltips showing variant labels (wildtype+site+mutant) and titer values
  - Click to highlight points
- **Statistics**: Pearson correlation coefficient displayed in bottom right corner of each plot
- **Styling**: Clean appearance with no background grid lines or borders

## Usage

1. Ensure input data is available at the path specified in `config.yaml`
2. Run the analysis script:
   ```bash
   python entry_black_dots.py
   ```
3. Open `entry_correlation_plots.html` in a web browser to view interactive plots

## Dependencies

- pandas: Data manipulation and analysis
- altair: Statistical visualization
- numpy: Numerical computing
- scipy.stats: Statistical functions (Pearson correlation)
- yaml: Configuration file parsing

## Data Processing

The script automatically:
- Loads entry titer data from the configured CSV file
- Creates variant labels by concatenating wildtype, site, and mutant information
- Removes rows with missing values in any of the four cell lines of interest
- Calculates Pearson correlation coefficients for all pairwise comparisons
- Generates interactive visualizations with hover tooltips and correlation statistics