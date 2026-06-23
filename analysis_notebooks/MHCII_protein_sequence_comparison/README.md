# MHCII Protein Sequence Identity Analysis

This analysis calculates pairwise protein sequence identity between MHCII alpha and beta chains and creates heatmap visualizations similar to Figure 1b from [academic.oup.com/ve/article/12/1/veag018/8534428](https://academic.oup.com/ve/article/12/1/veag018/8534428).

## Files

- `mhcii_sequence_identity_heatmap.py`: Main script for sequence identity analysis
- `requirements.txt`: Required Python packages
- `plots/`: Output directory containing generated heatmaps and data files

## Generated Outputs

### Heatmaps
- `mhcii_alpha_chain_identity_heatmap.svg`: Alpha chain sequence identity heatmap (vector format)
- `mhcii_beta_chain_identity_heatmap.svg`: Beta chain sequence identity heatmap (vector format)

### Data Files
- `alpha_chain_identity_matrix.csv`: Alpha chain pairwise identity percentages
- `beta_chain_identity_matrix.csv`: Beta chain pairwise identity percentages

## Key Results

### Alpha Chain Identities
- Human MHCII variants show very high identity (99.6-100%)
- Tufted duck MHCII shows 62% identity to all human variants
- Mean identity: 84.7% (range: 62.0% - 100.0%)

### Beta Chain Identities
- Human MHCII variants show high but more variable identity (91.0-94.0%)
- Tufted duck MHCII shows 52.9-56.4% identity to human variants
- Mean identity: 77.2% (range: 52.9% - 94.0%)

## Key Findings

1. **Species Conservation**: Both alpha and beta chains show clear species-specific clustering, with human sequences being highly similar to each other but divergent from tufted duck.

2. **Chain-Specific Variation**: Alpha chains are more conserved between human variants than beta chains, suggesting different evolutionary pressures.

3. **Interspecies Divergence**: The ~62% alpha chain and ~53-56% beta chain identity between human and tufted duck sequences indicates substantial evolutionary divergence.

## Usage

```bash
# Install dependencies
pip install -r requirements.txt

# Run analysis
python mhcii_sequence_identity_heatmap.py
```

## Method

The script uses Biopython's pairwise sequence alignment to calculate sequence identity:
1. Performs optimal pairwise alignment between protein sequences
2. Counts identical amino acid positions (excluding gaps)
3. Calculates percentage identity as (identical positions / total aligned positions) × 100
4. Creates symmetric matrices and visualizes as heatmaps using matplotlib/seaborn

The visualization uses a compact lower-triangle heatmap format with a custom teal color palette (white to #0081A7), smaller squares, and large white bold percentage annotations that fully fill each cell for optimal readability.