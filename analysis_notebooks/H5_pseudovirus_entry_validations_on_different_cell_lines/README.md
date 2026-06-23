# H5 Pseudovirus Entry Validations on Different Cell Lines

This notebook plots titers of H5 pseudovirus variants on different cell lines.

## Project Structure

```
H5_pseudovirus_entry_validations_on_different_cell_lines/
├── virus_titers.ipynb                        # Main analysis notebook
├── virus_titers_by_variant.html              # Output visualization by variant
├── increase_over_noSA_by_variant.html        # Output fold-change visualization
├── virus_titers.html                         # Output combined visualization
├── virus_titers.csv                          # Processed titer data output
├── data/
│   └── virus_titer_RLU.csv                  # Input RLU titer data
└── README.md                                 # This documentation
```

## Input Files

- **`data/virus_titer_RLU.csv`**: Contains RLU measurements for virus titers

## Output Files

- **`virus_titers_by_variant.html`** : Interactive plot showing titers by variant
- **`increase_over_noSA_by_variant.html`** : Interactive plot showing fold-change analysis
- **`virus_titers.html`** : Interactive combined visualization
- **`virus_titers.csv`** : Processed titer data

## Usage

This notebook needs to be run manually.

```bash
jupyter notebook virus_titers.ipynb
```