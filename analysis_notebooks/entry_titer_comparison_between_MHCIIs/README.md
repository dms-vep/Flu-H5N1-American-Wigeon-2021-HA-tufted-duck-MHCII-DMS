# Entry Titer Comparison Between MHCIIs

This notebook plots titers of influenza pseudoviruses from different subtypes on different cell lines.

## Project Structure

```
entry_titer_comparison_between_MHCIIs/
├── virus_titers.ipynb                     # Main analysis notebook
├── virus_titers_by_strain.html           # Output visualization by strain
├── increase_over_noSA_by_strain.html     # Output fold-change visualization  
├── virus_titers.csv                      # Processed titer data output
├── data/
│   └── virus_titer_RLU.csv              # Input RLU titer data
└── README.md                             # This documentation
```

## Input Files

- **`data/virus_titer_RLU.csv`** (20KB): Contains RLU measurements for virus titers

## Output Files

- **`virus_titers_by_strain.html`** (11KB): Interactive plot showing titers by strain
- **`increase_over_noSA_by_strain.html`** (8KB): Interactive plot showing fold-change analysis
- **`virus_titers.csv`** (2KB): Processed titer data

## Usage

This notebook needs to be run manually.

```bash
jupyter notebook virus_titers.ipynb
```