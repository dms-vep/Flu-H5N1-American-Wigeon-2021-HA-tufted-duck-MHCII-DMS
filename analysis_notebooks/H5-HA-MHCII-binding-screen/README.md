# H5 HA MHCII Binding Screen - Virus Titer Analysis

This project processes virus titer data from 96-well plate experiments and generates interactive plots showing virus binding to different MHCII cell lines.

## Project Overview

This analysis measures the binding titers of H5 influenza hemagglutinin (HA) pseudotyped lentiviruses to various MHCII-expressing cell lines. The experimental setup uses 96-well plates with different virus strains tested against multiple cell line variants.

## Project Structure

### Folder Organization

```
project/
├── data/                    # Input files
│   ├── config.yaml         # Configuration settings
│   ├── IDs.csv            # Virus ID to strain mapping
│   ├── plate_layouts.csv  # Plate layout definitions
│   └── *.xlsx            # Raw experimental data files
├── results/                # Output files
│   ├── *.csv              # Processed data files
│   └── *.html            # Interactive visualizations
├── plot_virus_titers.py   # Main analysis script
└── README.md              # This documentation
```

### Input Files (data/ folder)

- **`config.yaml`**: Configuration file specifying:
  - `virus_volume_ul`: Volume of virus used in each well (µL)
  - `min_titers`: Minimum RLU/µL threshold for QC filtering
  - `plates`: List of Excel files to process

- **`IDs.csv`**: Mapping file with four columns:
  - `ID`: Numerical identifier (1-88)
  - `strain`: Full virus strain name (e.g., "A/Goose/Guangdong/1/96")
  - `clade`: H5 phylogenetic clade (e.g., "2.3.4.4b", "0", "EA_nonGsGD")
  - `protein_sequence`: H5 HA protein sequence (~568 amino acids)

- **`plate_layouts.csv`**: 96-well plate layout definitions showing which virus ID goes in each well:
  - `plate1`: IDs 1-30
  - `plate2`: IDs 31-59  
  - `plate3`: IDs 60-88
  - Layout format: rows A-H, columns r1-r12
  - `NA` indicates empty wells

- **Excel files** (`.xlsx`): Raw experimental data
  - Naming convention: `{plate}-{cell_line}.xlsx`
  - Examples: `plate1-293-noSA-tufted-duck-MHCII.xlsx`, `plate2-293-SA23.xlsx`
  - RLU data located in cells B11:M18 (corresponds to 96-well plate)

### Cell Lines Tested

Based on the configuration, the following cell lines are analyzed:
- `293-SA23`: 293 cells expressing sialic acid α2,3
- `293-noSA`: 293 cells without sialic acid
- `293-noSA-human-MHCII-0301`: 293 cells without sialic acid, expressing human MHCII HLA-DRB1*03:01
- `293-noSA-human-MHCII-1503`: 293 cells without sialic acid, expressing human MHCII HLA-DRB1*15:03
- `293-noSA-tufted-duck-MHCII`: 293 cells without sialic acid, expressing tufted duck MHCII

## Data Processing Pipeline

The analysis script (`plot_virus_titers.py`) performs the following steps:

1. **Load Configuration**: Read `config.yaml` for plates and virus volume
2. **Load Mappings**: Read ID-to-strain, clade, and protein sequence mapping from `IDs.csv`  
3. **Load Plate Layouts**: Parse 96-well plate layouts from `plate_layouts.csv`
4. **Process Excel Files**: For each plate:
   - Extract RLU values from B11:M18 range
   - Map plate positions to virus IDs using layout
   - Convert IDs to strain names, clade information, and protein sequences
   - Calculate RLU per µL by dividing by virus volume
5. **Aggregate Data**: Average RLU values across replicates for each strain-cellline combination
6. **Quality Control**: Filter viruses based on minimum titer threshold:
   - QC PASS: Viruses with titers > min_titers in ANY cell line (successfully rescued)
   - QC FAIL: Viruses with titers ≤ min_titers in ALL cell lines (rescue failed)
7. **Generate Plots**: Create interactive Altair visualizations for all data, QC pass, and QC fail groups

## Usage

### Requirements

```python
pandas
numpy
altair
openpyxl  # for reading Excel files
pyyaml
```

### Running the Analysis

```bash
python plot_virus_titers.py
```

### Output Files

#### Data Files
- **`virus_titer_raw_data.csv`**: Raw extracted data with individual measurements (includes protein sequences)
- **`virus_titer_aggregated.csv`**: Aggregated data (mean RLU/µL per strain-cellline, includes protein sequences)
- **`virus_titer_with_errors.csv`**: Aggregated data with error bars (standard error of the mean, includes protein sequences)
- **`virus_titer_QC_pass.csv`**: Data for viruses that passed QC (successfully rescued, includes protein sequences)
- **`virus_titer_QC_fail.csv`**: Data for viruses that failed QC (rescue failed, includes protein sequences)
- **`virus_titer_fold_changes.csv`**: Fold-change analysis vs 293-noSA baseline (QC pass only, includes protein sequences)

#### Visualization Files
- **`virus_titers_processed.html`**: Interactive faceted plot (6 strains per row) - all data
- **`virus_titers_combined.html`**: Interactive combined plot with error bars and hover lines - all data
- **`virus_titers_combined_QC_pass.html`**: Combined plot showing only successfully rescued viruses (axis: 100 to 10,000,000 RLU/µL)
- **`virus_titers_combined_QC_fail.html`**: Combined plot showing only viruses with failed rescue
- **`virus_titers_fold_change.html`**: Fold-change plot vs 293-noSA baseline (QC pass only)
- **`virus_titers_cell_line_scatter.html`**: Cell line scatter plot with jitter and median indicators (QC pass only)
- **`virus_titers_fold_change_scatter.html`**: Fold change scatter plot with jitter and median indicators (QC pass only)

## Plot Descriptions

### Faceted Plot (`virus_titers_processed.html`)
A multi-panel scatter plot where:
- **Layout**: 6 virus strains per row with automatic wrapping
- **X-axis**: Different cell lines (shared across panels)
- **Y-axis**: RLU per µL (log scale, shared across panels)
- **Facets**: Separate panel for each virus strain
- **Points**: Mean titer values
- **Colors**: Different virus strains
- **Tooltips**: Hover for exact values

### Combined Plot (`virus_titers_combined.html`)
A horizontal scatter plot with trend lines where:
- **X-axis**: RLU per µL (log scale)
- **Y-axis**: Virus strains (grouped by phylogenetic clade)
- **Points**: Mean titer values with error bars (standard error)
- **Colors**: Different cell lines
- **Interactive Lines**: Hover over any point to highlight trend lines for that cell line
- **Error Bars**: Standard error of the mean across replicates
- **Clade Labels**: Visual grouping shows phylogenetic relationships
- **Tooltips**: Detailed information including clade, cell line, and replicate counts

### Fold-Change Plot (`virus_titers_fold_change.html`)
A comparative analysis plot showing enhanced/reduced binding vs control:
- **X-axis**: Fold-change vs 293-noSA baseline (log scale, automatically sized to data range)
- **Y-axis**: Virus strains (grouped by phylogenetic clade)
- **Data**: QC pass viruses only (successfully rescued)
- **Baseline**: 293-noSA cells (fold-change = 1.0 reference)
- **Points**: Fold-change values with propagated error bars
- **Colors**: Different cell lines
- **Interactive Lines**: Hover over any point to highlight trend lines for that cell line
- **Interpretation**: Values >1 indicate enhanced binding, <1 indicate reduced binding vs control
- **Error Propagation**: Standard errors calculated using error propagation theory
- **Auto-scaling**: Axis range automatically adjusts to actual data (currently ~0.5x to ~13,800x)
- **Intelligent Ticks**: Axis tick marks automatically generated based on data range
- **Tooltips**: Show fold-change, original titers, baseline titers, and error estimates

### Cell Line Scatter Plot (`virus_titers_cell_line_scatter.html`)
A clean scatter plot focusing on cell line comparisons:
- **X-axis**: Cell lines (5 different MHCII-expressing variants)
- **Y-axis**: Virus titers (RLU/µL, log scale)
- **Data**: QC pass viruses only (80 successfully rescued viruses)
- **Jitter**: Horizontal scatter within each cell line to prevent overlapping (400 total points)
- **Visual Style**: Large circles (size 150) with white outlines, no background grid lines
- **Median Indicators**: Black horizontal tick marks and text labels showing median titer for each cell line
- **Interactive Hover**: Gray connection lines appear when hovering over points, linking the same virus strain across all cell lines
- **Colors**: Each cell line has its distinct color for easy identification
- **Tooltips**: Virus strain, clade, titer values, SEM, and replicate counts
- **Purpose**: Compare absolute binding levels and distributions across cell line variants

### Fold Change Scatter Plot (`virus_titers_fold_change_scatter.html`)
A normalized comparison plot with the same visual style:
- **X-axis**: Cell lines (4 variants, excluding 293-noSA baseline)
- **Y-axis**: Fold change vs 293-noSA (log scale)
- **Data**: QC pass viruses only, normalized to 293-noSA control (320 total points)
- **Jitter**: Horizontal scatter within each cell line to prevent overlapping
- **Visual Style**: Large circles (size 150) with white outlines, no background grid lines
- **Median Indicators**: Black horizontal tick marks and text labels showing median fold change for each cell line
- **Interactive Hover**: Gray connection lines appear when hovering over points, linking the same virus strain across all cell lines
- **Colors**: Each cell line has its distinct color for easy identification
- **Tooltips**: Virus strain, clade, fold change values, SEM, original and baseline titers, replicate counts
- **Purpose**: Compare relative binding enhancement/reduction patterns independent of overall virus fitness
- **Interpretation**: Values >1.0 indicate enhanced binding, <1.0 indicate reduced binding vs 293-noSA control

## Data Quality Notes

- Wells marked as "NA" in plate layouts are excluded
- Replicates are averaged for final titer calculations
- Missing or invalid RLU values are filtered out
- Log scale is used for y-axis due to wide range of titer values

## Example Experimental Design

Each virus strain is tested in duplicate across the plate layout:
- Plate 1: Virus IDs 1-30 (strains like A/Goose/Guangdong/1/96, A/Hong_Kong/483/1997)
- Plate 2: Virus IDs 31-59 (continuing with more recent isolates)  
- Plate 3: Virus IDs 60-88 (most recent strains including 2024 isolates)

Cell lines test different binding specificities:
- **293-SA23**: Baseline binding with α2,3-linked sialic acids
- **293-noSA**: Control without sialic acid receptors
- **293-noSA-human-MHCII-0301/1503**: Human MHCII-dependent binding
- **293-noSA-tufted-duck-MHCII**: Avian MHCII-dependent binding

## Quality Control

### QC Methodology

The analysis includes quality control filtering to identify successfully rescued viruses:

- **QC Threshold**: Defined by `min_titers` parameter in config.yaml (default: 1000 RLU/µL)
- **QC Logic**: A virus passes QC if it achieves titers greater than the threshold in ANY cell line
- **Rationale**: Successfully rescued viruses should show detectable infectivity in at least one cell line

### QC Categories

- **QC PASS**: Viruses that exceeded the minimum titer threshold in at least one cell line
  - Indicates successful virus rescue and replication competency
  - Suitable for comparative binding analysis across cell lines
  
- **QC FAIL**: Viruses that failed to exceed the threshold in all cell lines
  - May indicate failed virus rescue, low viability, or technical issues
  - Excluded from binding preference analysis to avoid artifacts

### Current Results (Example)

Based on the 1000 RLU/µL threshold:
- **80 viruses passed QC** (successfully rescued)
- **7 viruses failed QC** (rescue issues)

Failed viruses include:
- A/Beijing/01/2003 (clade 7)
- A/bovine/Ohio/B24OSU439/2024 (clade 2.3.4.4b) 
- A/Cambodia/SVH240441/2024 (clade 2.3.2.1e)
- A/chicken/England/053052/2021 (clade 2.3.4.4b)
- A/duck/Hunan/70/2004 (clade 2.3.1)
- A/duck/Vietnam/NCVD-1494/2012 (clade 2.3.2.1a)
- A/mandarin duck/Korea/H71/2017 (clade 2.3.4.4b)

## Interpretation

### Titer Analysis
Higher RLU per µL values indicate stronger binding/infectivity of the virus to that particular cell line. Comparing values across cell lines for the same virus reveals:

- **Sialic acid dependency**: Compare 293-SA23 vs 293-noSA
- **MHCII specificity**: Compare different MHCII variants vs 293-noSA control
- **Species specificity**: Compare human vs tufted duck MHCII variants

### Interactive Features
- **Faceted plot**: Ideal for comparing cell line preferences for individual strains
- **Combined plot**: Best for identifying patterns across the entire virus panel
- **Fold-change plot**: Optimal for quantifying relative binding enhancements/reductions vs control
- **Cell line scatter plot**: Perfect for comparing distributions and median values across cell lines
- **Fold change scatter plot**: Ideal for visualizing relative binding patterns with median comparisons
- **Hover lines**: Reveal trends in cell line specificity across chronological virus evolution
- **Strain connection lines**: Scatter plots show gray lines connecting same virus across cell lines when hovering
- **Error bars**: Indicate experimental noise and data quality for each measurement

### Comparative Analysis Workflows

**Absolute Binding Assessment (Combined Plot):**
- Use `virus_titers_combined_QC_pass.html` for absolute titer comparisons
- Identify viruses with highest overall binding across all cell lines
- Compare binding magnitudes between virus clades

**Relative Binding Enhancement (Fold-Change Plot):**
- Use `virus_titers_fold_change.html` for normalized comparisons vs 293-noSA baseline
- Identify cell lines with enhanced receptor utilization (fold-change >1)
- Quantify MHCII-specific binding enhancements independent of overall virus fitness
- Compare relative binding preferences across phylogenetically diverse viruses

**Cell Line Distribution Analysis (Scatter Plots):**
- Use `virus_titers_cell_line_scatter.html` for absolute titer distribution comparisons across cell lines
- Use `virus_titers_fold_change_scatter.html` for normalized fold-change distribution comparisons
- Hover over points to trace individual virus strain patterns across all cell lines
- Compare median values (black tick marks and labels) to assess typical cell line performance
- Identify cell lines with consistent vs variable binding profiles

**Individual Strain Tracking (Interactive Hover):**
- Hover over any point in scatter plots to reveal gray connection lines for that specific virus strain
- Track how individual viruses perform across different cell line variants
- Identify viruses with unique binding preferences or consistent patterns
- Compare absolute vs relative binding profiles for the same strain

**Quality Assessment:**
- Review `virus_titers_combined_QC_fail.html` to assess rescue success rates by clade
- Use QC metrics to identify potential technical issues or biological constraints