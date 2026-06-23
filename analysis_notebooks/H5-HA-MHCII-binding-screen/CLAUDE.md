# Claude Code Assistance Log

This file tracks AI assistance provided by Claude Code for the H5 HA MHCII binding screen virus titer analysis project.

## Session: 2026-04-08

### Request
User requested creation of a script to generate virus titer plots in Altair format, similar to the example shown in `virus_titers_by_strain.html`.

### Data Structure Analysis
**Files examined:**
- `virus_titers_by_strain.html` - Example plot showing faceted scatter plot of virus titers
- `virus_titers.ipynb` - Existing notebook with Altair plotting code
- `config.yaml` - Configuration with virus volume and plate list
- `IDs.csv` - Mapping of numerical IDs to virus strain names (88 strains)
- `plate_layouts.csv` - 96-well plate layouts for plates 1-3
- Excel files (`*.xlsx`) - Raw RLU data in B11:M18 cells

**Data structure understood:**
- IDs 1-88 map to virus strains from 1996-2025 H5 isolates
- 3 plate layouts with IDs distributed across 96-well format
- Excel files named as `{plate}-{cell_line}.xlsx`
- RLU measurements in specific Excel range (B11:M18)
- Need to calculate RLU per µL by dividing by virus volume

### Solution Implemented

**Created files:**

1. **`plot_virus_titers.py`** - Main processing script
   - Reads config.yaml for plates and virus volume
   - Loads ID-to-strain mapping from IDs.csv
   - Parses 96-well plate layouts
   - Extracts RLU data from Excel files (B11:M18 range)
   - Maps plate positions to virus IDs and strains
   - Calculates RLU per µL values
   - Aggregates replicates by taking means
   - Generates Altair faceted scatter plot
   - Saves processed data and interactive HTML plot

2. **`README.md`** - Comprehensive documentation
   - Project overview and experimental design
   - Detailed file descriptions
   - Data processing pipeline explanation
   - Usage instructions and requirements
   - Output file descriptions
   - Interpretation guidelines

3. **`CLAUDE.md`** - This assistance log

### Key Features of the Script

**Data Processing:**
- Robust Excel file reading with error handling
- Flexible plate layout parsing supporting 3 plates
- ID-to-strain mapping with data validation
- Replicate averaging for final titer calculations
- Export of both raw and aggregated data

**Visualization:**
- Altair-based interactive plot matching example format
- Faceted design with one panel per virus strain
- Log-scale y-axis for RLU per µL values
- Color coding by virus strain
- Customizable ordering of viruses and cell lines
- Tooltips showing exact values on hover

**Output:**
- `virus_titer_raw_data.csv` - Individual measurements
- `virus_titer_aggregated.csv` - Mean values per strain-cellline
- `virus_titers_processed.html` - Interactive plot

### Technical Decisions

1. **Excel Reading**: Used `openpyxl` via `pandas.read_excel()` for robust .xlsx handling
2. **Layout Parsing**: Custom parser to handle the multi-plate format in `plate_layouts.csv`
3. **Data Structure**: Maintained compatibility with existing notebook's data format
4. **Error Handling**: Graceful handling of missing files, invalid data, unmapped IDs
5. **Modularity**: Functions separated for config loading, data processing, and plotting

### Code Quality
- Comprehensive docstrings for all functions
- Type-safe data operations with pandas
- Categorical data types for proper ordering in plots
- Configuration-driven processing for flexibility
- Clear variable naming and code structure

### Usage
The script is designed to be run with:
```bash
python plot_virus_titers.py
```

No command-line arguments required - all configuration read from `config.yaml`.

### Testing and Results

**Test Run Results (2026-04-08):**
- ✅ Successfully processed all 4 Excel files from config.yaml
- ✅ Extracted 236 total data points (60 from each plate1 file, 58 from each plate2 file)
- ✅ Identified 59 unique virus strains across H5 lineage (1996-2025 isolates)
- ✅ Processed 2 cell lines: `293-SA23` and `293-noSA-tufted-duck-MHCII`
- ✅ Generated aggregated data with 118 strain-cellline combinations
- ✅ Created interactive Altair plot matching example format

**Initial Issues Resolved:**
1. **Plate layout parsing bug**: Fixed CSV reading to handle `plate1` correctly by using `header=None`
2. **Filename parsing**: Improved extraction of plate number from Excel filenames

**Output Files Generated:**
- `virus_titer_raw_data.csv`: Individual RLU measurements (236 rows)
- `virus_titer_aggregated.csv`: Mean RLU/µL per strain-cellline (118 rows) 
- `virus_titers_processed.html`: Interactive faceted scatter plot

### Plot Layout Customizations (Session 2)

**User Request**: Modify plot layout to show 6 viruses per row with shared x-axis instead of all viruses in a single row.

**Changes Made:**
1. **Facet Layout**: Updated from `.facet(column=...)` to `.facet(alt.Facet(...), columns=6)` 
2. **Row Wrapping**: Implemented automatic wrapping every 6 virus strains
3. **Shared Axes**: Added `x="shared"` and `y="shared"` in `resolve_scale()`
4. **Panel Sizing**: Adjusted width to 160px to accommodate 6 columns
5. **Header Configuration**: Moved header styling to `.configure_header()`

**Final Plot Layout:**
- 6 virus strains per row with automatic wrapping to new rows
- ~10 rows total for 59 virus strains (9 full + 1 partial)
- Shared x-axis (cell lines) and y-axis (RLU per µL log scale)
- Consistent spacing and responsive design

**Current Status**: ✅ Script fully functional with custom layout
- All 15 Excel files processed successfully (expanded from 4)
- 88 H5 virus strains from 1996-2025 displayed across multiple rows
- Interactive HTML plot with improved readability and comparison capability

### Combined Plot with Error Bars (Session 3)

**User Request**: Create a new plot showing all titer data on one plot colored by cell line, similar to flu-seqneut example, with error bars and hover-activated trend lines.

**Changes Made:**
1. **New aggregation function**: `aggregate_with_error_bars()` calculates standard error of mean
2. **New plotting function**: `create_combined_titer_plot()` creates horizontal scatter plot
3. **Plot layout**: Viruses on y-axis, titers on x-axis (log scale), colored by cell line
4. **Error bars**: Standard error of mean showing measurement noise between replicates
5. **Interactive hover**: Lines connecting same cell line points only appear on hover
6. **Clean default view**: No lines visible by default to avoid clutter

**Plot Features:**
- **Horizontal layout**: Similar to flu-seqneut example with viruses listed vertically
- **5 cell lines** color-coded: 293-SA23, 293-noSA, 293-noSA-human-MHCII variants
- **Error bars**: Show standard error of mean for each strain-cellline combination
- **Hover functionality**: Point over any cell line reveals trend line across all virus strains
- **Dynamic sizing**: Height adjusts for 88 virus strains
- **Tooltips**: Show exact values, SEM, and replicate counts

**Output Files:**
- `virus_titers_combined.html`: New horizontal scatter plot with error bars
- `virus_titer_with_errors.csv`: Data with calculated error bars and bounds

**Current Status**: ✅ Both plot types functional
- Faceted plot: 6 viruses per row across ~15 rows
- Combined plot: All viruses in single horizontal view with interactive hover trends

### Hover Line Implementation and Code Cleanup (Session 4)

**User Request**: Fix hover lines to only appear on mouseover, then clean up code and documentation.

**Issues Resolved:**
1. **Hover lines visible by default**: Multiple attempts with different selection parameters failed
2. **Final solution**: Adopted working pattern from flu-seqneut repository
3. **Key parameters**: `empty=False`, `clear='mouseout'`, `nearest=False`
4. **Line styling**: Faint by default (opacity=0.2, strokeWidth=0.5), thick on hover (opacity=0.8, strokeWidth=4)

**Final Working Code:**
```python
hover = alt.selection_point(fields=['cell_line'], on='mouseover', empty=False, clear='mouseout', nearest=False)
opacity=alt.condition(hover, alt.value(0.8), alt.value(0.2))
strokeWidth=alt.condition(hover, alt.value(4), alt.value(0.5))
```

**Code Cleanup:**
1. **Enhanced docstrings**: Added comprehensive script description
2. **Removed redundancies**: Eliminated duplicate numpy import
3. **Streamlined main()**: Consolidated output messages, improved flow
4. **Organized structure**: Better function organization and consistent formatting

**Documentation Updates:**
1. **README.md**: Added combined plot description, updated cell lines list, enhanced interpretation
2. **CLAUDE.md**: Documented complete session including successful hover implementation
3. **Final outputs**: Both CSV files and HTML plots with clean, production-ready code

**Final Status**: ✅ Production-ready analysis pipeline
- 88 H5 virus strains (1996-2025) across 5 MHCII cell lines
- Dual visualization approach: faceted + combined plots
- Interactive hover functionality working correctly
- Clean, documented codebase ready for publication/sharing

### Clade Grouping Implementation (Session 5)

**User Request**: Group strains by clade in the combined plot using updated IDs.csv with clade column.

**Changes Made:**
1. **Updated data loading**: Modified `load_id_mapping()` to return both strain and clade mappings
2. **Enhanced data processing**: Updated `process_plate_data()` to include clade information in extracted data
3. **Improved aggregation**: Modified aggregation functions to preserve clade information
4. **Clade-grouped ordering**: Created `create_virus_order_by_clade()` to sort strains by clade
5. **Visual enhancements**: Added clade labels to combined plot for clear grouping visualization
6. **Enhanced tooltips**: Included clade information in hover tooltips

**New Features:**
- **Phylogenetic organization**: Virus strains automatically grouped by H5 clade (2.3.4.4b, 2.2.1, etc.)
- **Clade diversity**: Handles diverse clades including numeric (0, 1, 2.3.4.4b) and geographic (EA_nonGsGD, Am_nonGsGD)
- **Visual clade labels**: Gray labels on chart indicate clade boundaries
- **Enhanced tooltips**: Hover shows virus strain, clade, cell line, titers, SEM, and replicate count

**Technical Implementation:**
- Updated CSV structure: ID, strain, clade columns
- Dual mapping system: separate dictionaries for strain names and clade assignments
- Flexible sorting: clades sorted alphabetically, strains sorted within each clade
- Backward compatibility: group_by_clade parameter allows toggling clade grouping

**Current Status**: ✅ Enhanced phylogenetic visualization
- 87 H5 virus strains across multiple clades (1996-2025)
- Phylogenetically-informed visualization reveals evolutionary patterns
- Maintains all previous interactive features with added clade context

### Quality Control Filtering Implementation (Session 6)

**User Request**: Add QC filtering based on minimum titer thresholds to identify successfully rescued viruses vs failed rescues, with separate plots for each group.

**Changes Made:**

1. **Enhanced Configuration**: Updated config.yaml to include `min_titers` parameter (1000 RLU/µL)

2. **QC Filtering Function**: Created `qc_filter_viruses()` that:
   - Calculates maximum titer for each virus across all cell lines
   - Classifies viruses as PASS (>threshold in ANY cell line) or FAIL (≤threshold in ALL cell lines)
   - Separates data into pass/fail datasets for visualization

3. **Separate Visualizations**: 
   - `virus_titers_combined_QC_pass.html`: Only successfully rescued viruses
   - `virus_titers_combined_QC_fail.html`: Only viruses with rescue failures
   - Original plots maintained showing all data

4. **Enhanced Output**:
   - `virus_titer_QC_pass.csv`: Data for 80 viruses that passed QC
   - `virus_titer_QC_fail.csv`: Data for 7 viruses that failed QC
   - Detailed QC summary in console output

5. **Plot Customization**: Added title suffixes to distinguish QC pass/fail plots

**QC Results (1000 RLU/µL threshold):**
- **80 viruses PASSED**: Successfully rescued and replication-competent
- **7 viruses FAILED**: Rescue issues, low viability, or technical problems

**Failed Viruses:**
- A/Beijing/01/2003 (clade 7)
- A/bovine/Ohio/B24OSU439/2024 (clade 2.3.4.4b)
- A/Cambodia/SVH240441/2024 (clade 2.3.2.1e)
- A/chicken/England/053052/2021 (clade 2.3.4.4b)
- A/duck/Hunan/70/2004 (clade 2.3.1)
- A/duck/Vietnam/NCVD-1494/2012 (clade 2.3.2.1a)
- A/mandarin duck/Korea/H71/2017 (clade 2.3.4.4b)

**Technical Features:**
- Configurable QC threshold via config.yaml
- Robust filtering logic based on maximum titer across cell lines
- Maintains phylogenetic grouping in filtered plots
- Clear visual distinction between QC categories

**Current Status**: ✅ Production-ready QC analysis pipeline
- Comprehensive virus rescue validation
- Separate analysis tracks for successful vs failed rescues
- Data-driven quality assessment for reliable downstream analysis

### Fold-Change Analysis Implementation (Session 6 continued)

**User Request**: Create additional plot showing fold-change in titers compared to 293-noSA baseline, for QC pass viruses only.

**Changes Made:**

1. **Fold-Change Calculation Function**: Created `calculate_fold_changes()` that:
   - Calculates fold-change as (test cell line RLU/µL) / (293-noSA RLU/µL)
   - Applies error propagation theory for fold-change standard errors
   - Handles baseline values to avoid division by zero
   - Includes baseline (293-noSA) as fold-change = 1.0 reference

2. **Fold-Change Visualization**: Created `create_fold_change_plot()` featuring:
   - Log-scale x-axis for fold-change values (0.01 to 100)
   - Phylogenetic grouping by clade (consistent with other plots)
   - Red dashed reference line at fold-change = 1.0
   - Color-coded by cell line with interactive hover lines
   - Error bars using propagated standard errors
   - Comprehensive tooltips with original and baseline titers

3. **Data Processing Enhancement**:
   - Applied fold-change analysis only to QC pass data (80 viruses)
   - Excluded failed rescue viruses to ensure reliable fold-change calculations
   - Maintained clade grouping and interactive features

4. **New Output Files**:
   - `virus_titer_fold_changes.csv`: Fold-change data with error propagation
   - `virus_titers_fold_change.html`: Interactive fold-change visualization

**Technical Features:**
- **Error Propagation**: σ_fc = fc * sqrt((σ_test/test)² + (σ_baseline/baseline)²)
- **Log Scale**: Handles wide range of fold-changes (0.01x to 100x)
- **Reference Line**: Clear visual indicator for no change (fold-change = 1)
- **Baseline Integration**: 293-noSA included as reference points
- **Quality Filter**: Only reliable, QC-passed viruses analyzed

**Analytical Value:**
- **Normalized Comparisons**: Removes virus-specific fitness effects
- **Enhanced Binding Detection**: Identifies cell line-specific enhancements >1x
- **Reduced Binding Detection**: Identifies cell line-specific reductions <1x
- **Cross-Clade Analysis**: Enables comparison across phylogenetically diverse viruses

**Sample Results:**
- A/American_Wigeon/South_Carolina/22-000345-001/2021: 712x enhancement with tufted duck MHCII
- A/Anhui/1/2005: 2308x enhancement with tufted duck MHCII, moderate enhancement with human MHCII
- Clear species-specific patterns emerging in fold-change data

**Current Status**: ✅ Comprehensive binding analysis pipeline
- Absolute titer analysis (combined plots)
- Relative fold-change analysis (normalized to 293-noSA)
- Quality-filtered datasets for reliable interpretation
- Phylogenetic organization revealing evolutionary patterns

### Dynamic Axis Scaling Enhancement (Session 6 continued)

**User Request**: Set fold-change plot axis based on actual min/max data values with padding, rather than hard-coded ranges.

**Changes Made:**

1. **Dynamic Range Calculation**: Added automatic calculation of axis bounds based on actual data:
   - `min_fold_change` and `max_fold_change` from filtered dataset
   - 20% padding in log space (multiply/divide by 1.2) for visual breathing room
   - Axis range: 0.4964 to 16,584.63 (data range: 0.5956 to 13,820.52)

2. **Intelligent Tick Generation**: Created algorithm to generate appropriate tick values:
   - Calculates reasonable powers of 10 within the data range
   - Adds intermediate values (2×, 5×) for better resolution
   - Generated ticks: [0.5, 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000]

3. **Adaptive Implementation**: Updated all scale references to use calculated values:
   - Error bars scale domain
   - Line chart scale domain  
   - Point chart scale domain
   - Reference line scale domain
   - Axis tick values

4. **Error Bound Safety**: Updated lower bound calculation to prevent log scale issues:
   - Changed from hard-coded 0.75 to dynamic 0.01 minimum
   - Ensures error bars never create invalid log scale values

**Technical Benefits:**
- **Future-proof**: Automatically adapts to different datasets
- **Optimal Resolution**: Maximizes plot space usage for actual data range
- **Clean Visualization**: No wasted space on non-existent data ranges
- **Intelligent Ticks**: Readable tick marks appropriate for the scale

**Visual Impact:**
- No more arbitrary scale limits (previous: 0.75 to 15,000)
- Perfect fit to actual data range (current: ~0.5 to ~16,600 with padding)
- Clean, readable axis labels at meaningful intervals
- Data points never touching axis boundaries

**Current Status**: ✅ Production-ready adaptive visualization pipeline
- Dynamic scaling ensures optimal plot resolution regardless of data range
- Intelligent tick generation provides clean, readable axis labels
- Future datasets automatically get appropriate axis scaling without code changes

### Final Visual Polish (Session 6 continued)

**User Requests**: Move legend and clade labels to the right; remove reference line at fold-change = 1.

**Changes Made:**

1. **Legend Positioning Enhancement**: Added `offset=50` parameter to legend configurations
   - Moves legends 50 pixels to the right of default position
   - Applied to both error bars and points legends in fold-change plot
   - Prevents overlap with data points and axis labels

2. **Clade Label Adjustment**: Fine-tuned clade label positioning through iterative refinement
   - Initial: `dx=550` → `dx=700` (too far right, overlapped legend)
   - Refined: `dx=700` → `dx=630` → `dx=610` → `dx=590` (final optimal position)
   - Achieves perfect balance between plot association and legend clearance
   - Maintains readability while providing clean visual separation

3. **Reference Line Removal**: Eliminated the red dashed reference line at fold-change = 1.0
   - Removed `reference_line` creation and chart layer addition
   - Simplifies plot visualization while maintaining interpretability
   - 293-noSA baseline points still clearly visible at fold-change = 1.0

**Visual Impact:**
- **Cleaner layout**: No overlap between legends, labels, and data
- **Better spacing**: All elements properly positioned with adequate breathing room
- **Simplified aesthetic**: Removed visual clutter while maintaining functionality
- **Professional appearance**: Clean, publication-ready visualization

**Technical Implementation:**
- Legend `offset` parameter for precise positioning
- Clade label `dx` adjustment for optimal placement
- Removed unnecessary reference line code and chart layer reference

**Current Status**: ✅ Final production-ready visualization suite
- Optimal axis scaling based on actual data
- Clean, professional layout with proper element spacing
- No visual overlaps or clutter
- Publication-ready fold-change analysis plots

### Custom Axis Scaling for QC Pass Plot (Session 7)

**User Request**: Set axis limits for virus_titers_combined_QC_pass plot between 100 and 10,000,000 RLU/µL.

**Changes Made:**

1. **Enhanced Function Parameters**: Modified `create_combined_titer_plot()` to accept optional `axis_domain` parameter
   - Default domain remains [10, 1e8] for compatibility with existing plots
   - Allows custom axis scaling for specific visualizations

2. **Updated All Scale References**: Replaced hard-coded domain values throughout the function:
   - Error bars scale domain: `[10, 1e8]` → `axis_domain`
   - Line chart scale domain: `[10, 1e8]` → `axis_domain`
   - Point chart scale domain: `[10, 1e8]` → `axis_domain`

3. **QC Pass Plot Customization**: Updated QC pass plot call to use custom axis limits:
   - Changed from default domain to `axis_domain=[100, 1e7]`
   - Provides focused view on successfully rescued virus titer range
   - Eliminates visual noise from very low titer values

**Technical Benefits:**
- **Focused Resolution**: QC pass plot optimizes space for meaningful titer range
- **Backward Compatibility**: Other plots maintain original scaling
- **Flexible Design**: Easy to adjust axis limits for different datasets
- **Clear Visual Distinction**: QC pass plot emphasizes successful rescue data

**Current Status**: ✅ Enhanced visualization with custom axis scaling
- QC pass plot: 100 to 10,000,000 RLU/µL range for optimal resolution
- Other plots: Maintain standard 10 to 100,000,000 RLU/µL range
- Clean, focused visualization of successfully rescued viruses

### Interactive Scatter Plot Implementation (Session 8)

**User Request**: Create new scatter plots with cell lines on x-axis and virus titers on y-axis, with median annotations and interactive features.

### Scatter Plot Development

**Initial Implementation:**

1. **Cell Line Scatter Plot Function**: Created `create_cell_line_scatter_plot()` for absolute titer visualization
   - Y-axis: Virus titers (RLU/µL, log scale)
   - X-axis: Cell lines (5 MHCII-expressing variants)
   - Data: QC pass viruses only (400 data points: 80 viruses × 5 cell lines)
   - Output: `virus_titers_cell_line_scatter.html`

2. **Fold Change Scatter Plot Function**: Created `create_fold_change_scatter_plot()` for normalized comparison
   - Y-axis: Fold change vs 293-noSA (log scale)
   - X-axis: Cell lines (4 variants, excluding baseline)
   - Data: QC pass viruses only (320 data points: 80 viruses × 4 cell lines)
   - Output: `virus_titers_fold_change_scatter.html`

### Visual Enhancement Iterations

**Horizontal Jitter Implementation:**
- **Challenge**: Points overlapped vertically within each cell line category
- **Solution**: Added `transform_calculate` with `jittered_x="indexof(cell_order, datum.cell_line) + (random() - 0.5) * 0.6"`
- **Result**: Points spread horizontally within each cell line for better visibility

**Enhanced Visual Design:**
- **Point styling**: Size 150 circles with white outlines (`stroke='white', strokeWidth=1.5`)
- **Clean background**: Removed all grid lines (`grid=False` on both axes)
- **Median indicators**: Black horizontal tick marks and text labels showing median values
- **Color coding**: Each cell line has distinct color with legend

**Median Annotation Refinement:**
- **Position**: Black text labels positioned at top of plot (`dy=-2` for optimal spacing)
- **Format**: Scientific notation for titer plot (`.1e`), decimal for fold change plot (`.1f`)
- **Alignment**: Perfect alignment with corresponding cell line columns
- **Markers**: Solid black horizontal lines spanning ±0.25 units from cell line center

### Interactive Hover Features

**Strain Connection Lines:**
- **Implementation**: Added hover selection with `alt.selection_point(fields=['strain'], on='mouseover')`
- **Functionality**: Gray connection lines appear when hovering over any point
- **Purpose**: Connect all data points for the same virus strain across different cell lines
- **Styling**: Gray lines (`color='gray'`) with conditional opacity (`opacity=0.0` default, `0.7` on hover)

**Enhanced Tooltips:**
- **Cell line scatter**: Strain, clade, titer, SEM, replicate counts
- **Fold change scatter**: Strain, clade, fold change, SEM, test/baseline titers, replicate counts

### Technical Implementation Details

**Data Processing:**
- Categorical ordering with `CategoricalDtype` for proper x-axis labels
- Numeric position mapping for jitter calculations and median placement
- Hover selection with proper event handling (`empty=False, clear='mouseout'`)

**Chart Composition:**
- **Layer order**: Lines → scatter points → median markers → median text
- **Scale resolution**: `resolve_scale(color='independent')` to handle multiple color mappings
- **Interactive coordination**: Hover selection shared across line and point layers

**Axis Configuration:**
- **Quantitative x-axis**: Custom domain `[-0.5, len(cell_order) - 0.5]` for proper spacing
- **Label expression**: Complex `labelExpr` to map numeric positions back to cell line names
- **No grid styling**: Clean appearance without background grid interference

### Final Features

**Both Scatter Plots Include:**
- ✅ **400/320 data points**: All QC-passed viruses across cell line variants
- ✅ **Horizontal jitter**: Prevents overlapping, shows individual measurements
- ✅ **White-outlined circles**: Large, clearly visible points (size 150)
- ✅ **No grid lines**: Clean, minimal background
- ✅ **Black median indicators**: Horizontal tick marks + numeric labels
- ✅ **Interactive strain tracking**: Hover reveals gray connection lines
- ✅ **Detailed tooltips**: Comprehensive measurement information
- ✅ **Professional styling**: Publication-ready visualization

**Output Files:**
- `virus_titers_cell_line_scatter.html`: Absolute titer distributions
- `virus_titers_fold_change_scatter.html`: Normalized binding enhancements

**Current Status**: ✅ Complete interactive scatter plot suite
- Perfect visual consistency with existing plots
- Advanced interactive features for strain pattern analysis
- Clean, professional design suitable for publication
- Comprehensive documentation in README.md

### Future Enhancements Possible
- Command-line argument support for custom config files
- Statistical analysis integration
- Batch processing of multiple experiments
- Data validation and quality control metrics
- Custom virus ordering by chronological/phylogenetic criteria
- Export options (PNG, PDF, SVG)