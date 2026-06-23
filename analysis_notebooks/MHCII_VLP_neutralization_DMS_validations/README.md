# MHCII VLP Neutralization DMS Validations

This notebook fits Hill curves to VLP neutralization data for HA mutant variants and creates interactive neutralization curves.

## Project Structure

```
MHCII_VLP_neutralization_DMS_validations/
├── neuts_altair_dms_validations.ipynb           # Main analysis notebook
├── neutralization_curves_dms_validations.html   # Interactive neutralization plot
├── ICXX_dms_validations.csv                    # Fitted curve parameters
├── data/
│   └── fracinfect.csv                          # Input fraction infectivity data
└── README.md                                   # This documentation
```

## Analysis Workflow

The `neuts_altair_dms_validations.ipynb` notebook:

1. **Loads data** from `./data/fracinfect.csv` (160 rows with columns: serum, virus, replicate, concentration, fraction infectivity)

2. **Fits Hill curves** using neutcurve package to calculate IC50 and NT50 values for each virus variant

3. **Creates Altair visualization** with:
   - Line plots showing fitted curves
   - Error bars showing standard deviation across replicates
   - Scatter points showing mean data values
   - Log-scale x-axis (VLP dilution)
   - Custom color scheme with WT in black

## Input Data Format

The `fracinfect.csv` file contains:
- **serum**: tufted-duck-MHCII-gag-VLP
- **virus**: WT, A137S, R227G, T219E, Y256W, I80L, I80L_A137S_R227G, A137S_R227, D77E, R149T
- **replicate**: Replicate number
- **concentration**: VLP dilution concentration  
- **fraction infectivity**: Measured fraction infectivity value

## Output Files

### Neutralization Curves (`neutralization_curves_dms_validations.html`)
Interactive Altair plot showing:
- Fitted Hill curves for each virus variant
- Error bars representing standard deviation
- Mean data points for each concentration
- WT strain highlighted in black
- Tooltips with mean values, standard deviation, and replicate counts

## Requirements

```python
neutcurve>=2.3.0
altair>=6.0.0
pandas
numpy
```

## Usage

```bash
jupyter notebook neuts_altair_dms_validations.ipynb
```

Execute all cells to generate the HTML plot and CSV parameter file.