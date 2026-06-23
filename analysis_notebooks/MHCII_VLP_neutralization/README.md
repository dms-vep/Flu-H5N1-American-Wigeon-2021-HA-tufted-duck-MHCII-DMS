# MHCII VLP Neutralization

This notebook fits Hill curves to VLP neutralization data and creates interactive neutralization curves using the neutcurve package.

## Project Structure

```
MHCII_VLP_neutralization/
├── neuts_altair.ipynb              # Main analysis notebook
├── neutralization_curves.html      # Interactive neutralization plot
├── ICXX.csv                        # Fitted curve parameters
├── data/
│   └── fracinfect.csv             # Input fraction infectivity data
└── README.md                      # This documentation
```

## Analysis Workflow

The `neuts_altair.ipynb` notebook:

1. **Loads data** from `./data/fracinfect.csv` (40 rows with columns: serum, virus, replicate, concentration, fraction infectivity)

2. **Fits Hill curves** using neutcurve package to calculate IC50 values and NT50 values

3. **Generates smooth curves** with 200 points per virus for visualization

4. **Creates Altair visualization** with:
   - Line plots showing fitted curves
   - Scatter points showing raw data
   - Log-scale x-axis (VLP dilution)
   - Interactive tooltips

## Input Data Format

The `fracinfect.csv` file contains:
- **serum**: H5_293T 
- **virus**: gag+tufted-duck-MHCII, gag, tufted-duck-MHCII, cell_supernatant, cell_media
- **replicate**: Replicate number
- **concentration**: VLP dilution concentration
- **fraction infectivity**: Measured fraction infectivity value

## Output Files

### Neutralization Curves (`neutralization_curves.html`)
Interactive Altair plot showing:
- Fitted Hill curves for each virus condition
- Raw data points with error information
- Log-scale x-axis for concentration
- Color-coded by virus type
- Tooltips with detailed values

### Parameters (`ICXX.csv`)
Fitted curve parameters including:
- **ic50**: Half-maximal inhibitory concentration
- **ic50_bound**: Whether IC50 is interpolated, upper bound, or lower bound
- **NT50**: Neutralizing titer (1/ic50)

## Requirements

```python
neutcurve>=2.3.0
altair>=6.0.0
pandas
numpy
```

## Usage

```bash
jupyter notebook neuts_altair.ipynb
```

Execute all cells to generate the HTML plot and CSV parameter file.