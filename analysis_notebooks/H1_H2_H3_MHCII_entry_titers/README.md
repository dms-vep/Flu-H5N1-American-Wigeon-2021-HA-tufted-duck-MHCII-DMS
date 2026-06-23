# H1H2H3 HA MHCII Binding Screen Analysis

This repository contains analysis code and data for measuring virus titers across different MHCII-expressing cell lines to assess binding specificity of H1, H2, and H3 influenza A virus hemagglutinins.

## Overview

This analysis processes virus titer data from 96-well plate assays measuring binding of diverse influenza viruses (H1, H2, H3 subtypes) to different MHCII-expressing cell lines. The goal is to identify subtype-specific and host-specific binding patterns to MHCII molecules from different species.

## Experimental Design

**Virus Library**: 30 influenza virus strains spanning:
- **H1 subtype**: Swine, human, and avian isolates (1918-2016)
- **H2 subtype**: Human and avian isolates (1957-2008) 
- **H3 subtype**: Human, avian, swine, and equine isolates (1968-2025)

**Cell Lines**: 5 different MHCII-expressing 293T cell lines:
- `293-SA23`: Control with 2,3 linked dialic acid expression
- `293-SA26`: Control with 2,6 linked dialic acid expression
- `293-noSA`: Baseline control without SA expression
- `293-noSA-human-MHCII-0301`: Human MHCII allele 0301
- `293-noSA-human-MHCII-1503`: Human MHCII allele 1503
- `293-noSA-tufted-duck-MHCII`: Tufted duck MHCII

**Assay**: Relative Light Units (RLU) measured from 96-well plates, converted to RLU/µL using virus volume.

## Repository Structure

```
├── data/
│   ├── config.yaml              # Analysis configuration
│   ├── IDs.csv                  # Virus strain metadata and mappings
│   ├── plate_layouts.csv        # 96-well plate layout definitions
│   └── *.xlsx                   # Raw RLU data files (one per plate-cellline combination)
├── results/                     # Generated outputs (created by script)
├── plot_virus_titers.py        # Main analysis script
├── example.py                   # Reference implementation for jitter
└── README.md                   # This file
```

## Data Files

### Input Files

**`data/IDs.csv`**
- Virus strain metadata with columns: `ID`, `strain`, `host`, `subtype`, `Genbank`, `plasmid_log_no`, `protein_sequence`
- Maps numerical IDs (1-30) to virus strain information
- Includes host species, HA subtype, GenBank accession, and plasmid references

**`data/config.yaml`**
- Analysis parameters: virus volume, QC thresholds, plate list
- Currently processes 5 plates from plate1 data
- Excluded strains: 
	- `A/swine/Changhua/199-3/2000` we excluded this strain becasue it is not correctly dated, based on phylogenetic tree it clusters with classical A/swine/Iowa/15/1930 and so should be a ~1930s isolate. Indeed, its cell titer data looks like A/swine/Iowa/15/1930, suggesting it is also functionally similar.

**`data/plate_layouts.csv`** 
- 96-well plate layouts mapping well positions to virus IDs
- Format: rows A-H, columns 1-12, values are virus ID numbers

**`data/*.xlsx`**
- Raw luminescence data files named as `{plate}-{cell_line}.xlsx`
- RLU measurements in range B11:M18 (96-well plate format)

### Output Files

**CSV Data Files:**
- `virus_titer_raw_data.csv`: Individual RLU measurements with all metadata
- `virus_titer_aggregated.csv`: Mean RLU/µL per strain-cellline combination  
- `virus_titer_with_errors.csv`: Data with standard error calculations
- `virus_titer_QC_pass.csv`: Successfully rescued viruses (>1000 RLU/µL threshold)
- `virus_titer_QC_fail.csv`: Failed rescues or low-titer viruses
- `virus_titer_fold_changes.csv`: Fold-change analysis vs 293-noSA baseline

**Interactive HTML Plots:**
- `virus_titers_processed.html`: Faceted plot (6 viruses per row)
- `virus_titers_combined.html`: All data with subtype grouping and hover lines
- `virus_titers_combined_QC_pass.html`: QC-passed viruses only
- `virus_titers_combined_QC_fail.html`: Failed viruses only
- `virus_titers_fold_change.html`: Fold-change analysis with subtype grouping
- **Note**: Scatter plots have been disabled and are no longer generated

## Requirements

**Python Dependencies:**
```python
import os
import warnings
import yaml
import numpy as np
import pandas as pd
import altair as alt
from pandas.api.types import CategoricalDtype
```

**Install via conda/pip:**
```bash
pip install pandas numpy altair pyyaml openpyxl
```

## Usage

**Basic Analysis:**
```bash
python plot_virus_titers.py
```

The script automatically:
1. Reads configuration from `data/config.yaml`
2. Loads virus strain metadata and plate layouts
3. Processes Excel files and calculates RLU/µL values
4. Applies quality control filtering (1000 RLU/µL threshold)
5. Generates fold-change analysis vs 293-noSA baseline
6. Creates all visualization outputs

**No command-line arguments required** - all parameters are configured in `config.yaml`.

## Key Features

### Data Processing
- **Flexible plate layouts**: Handles multiple 96-well plate configurations
- **Replicate averaging**: Calculates means and standard errors across replicates
- **Quality control**: Automatic filtering of low-titer/failed rescues
- **Error propagation**: Proper statistical treatment of fold-change uncertainties

### Visualizations
- **Subtype grouping**: H1, H2, H3 viruses grouped phylogenetically 
- **Host shapes**: Point shapes indicate host species (swine, human, avian, equine)
- **Interactive features**: Hover tooltips, strain connection lines, subtype coloring
- **Multiple views**: Faceted, combined, and fold-change formats (scatter plots disabled)
- **Clean styling**: No grid lines, proper axis scaling, dashed separators

### Statistical Analysis
- **QC filtering**: Identifies successfully rescued vs failed viruses
- **Baseline normalization**: Fold-change analysis relative to 293-noSA
- **Error quantification**: Standard error of mean for all measurements
- **Replicate tracking**: Maintains information about sample sizes

## Output Interpretation

### QC Results
- **PASS**: Viruses with >1000 RLU/µL in ANY cell line (successfully rescued)
- **FAIL**: Viruses with ≤1000 RLU/µL in ALL cell lines (rescue failures)

### Fold-Change Analysis
- **Values >1**: Enhanced binding compared to 293-noSA baseline
- **Values <1**: Reduced binding compared to 293-noSA baseline  
- **Values ~1**: Similar binding to baseline control

### Scatter Plots
- **Status**: Scatter plots have been disabled in this analysis
- **Previous functionality**: Previously included jittered points, hover strain lines, and subtype/host grouping
- **Alternative**: Use the combined plots for similar visualization of relationships across cell lines

## Customization

### Configuration Options
Edit `data/config.yaml` to modify:
- `virus_volume_ul`: Volume used for RLU/µL calculations
- `min_titers`: QC threshold for successful rescue
- `plates`: List of Excel files to process

### Plot Customization
Key parameters in `plot_virus_titers.py`:
- Color palettes: `SUBTYPE_COLORS`, `CELL_COLORS`
- Axis ranges: Currently 10 to 2,000,000 RLU/µL
- Plot dimensions: Width/height settings
- Jitter amount: `(random() - 0.5) * 0.6` in transform_calculate

## Technical Notes

### Plate Layout Format
- Rows A-H correspond to wells 1-8 vertically
- Columns 1-12 correspond to wells 1-12 horizontally  
- `NA` indicates empty wells
- Numerical values map to virus IDs in `IDs.csv`

### Excel File Processing
- Reads range B11:M18 (8 rows × 12 columns = 96 wells)
- Handles missing files gracefully with warnings
- Converts all RLU values to float for calculations

### Memory and Performance
- Processes ~300 data points efficiently
- All calculations performed in pandas for speed
- Interactive plots use Vega-Lite for smooth rendering

## Troubleshooting

**Common Issues:**
1. **"File not found"**: Check that Excel files match names in `config.yaml`
2. **"No data processed"**: Verify plate layouts match Excel file structure
3. **"Empty plots"**: Check QC threshold - may be filtering all data

**Debug Steps:**
1. Verify `data/config.yaml` plate list matches available `.xlsx` files
2. Check `data/plate_layouts.csv` for correct plate identifier names
3. Confirm Excel files have data in range B11:M18
4. Review QC threshold if no viruses pass quality control

## Citation

If you use this analysis pipeline, please cite:
- The original experimental data source
- This computational analysis pipeline
- Key software dependencies: Python, Pandas, Altair

---

**Contact**: [Your contact information]  
**Last Updated**: April 2026  
**Version**: 1.0