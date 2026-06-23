#!/usr/bin/env python3
"""
Script to calculate protein sequence identity between MHCII alpha and beta chains
and create heatmaps similar to Figure 1b from academic.oup.com/ve/article/12/1/veag018/8534428
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
from Bio import Align
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from itertools import combinations
import os

# Configure matplotlib for proper SVG font rendering
plt.rcParams['svg.fonttype'] = 'none'

def calculate_sequence_identity(seq1, seq2):
    """
    Calculate sequence identity between two protein sequences using pairwise alignment.

    Args:
        seq1 (str): First protein sequence
        seq2 (str): Second protein sequence

    Returns:
        float: Sequence identity percentage (0-100)
    """
    if seq1 == seq2:
        return 100.0

    # Create aligner
    aligner = Align.PairwiseAligner()
    aligner.match_score = 2
    aligner.mismatch_score = -1
    aligner.open_gap_score = -2
    aligner.extend_gap_score = -0.5

    # Perform alignment
    alignments = aligner.align(seq1, seq2)
    best_alignment = alignments[0]

    # Count identical positions
    aligned_seq1 = str(best_alignment[0])
    aligned_seq2 = str(best_alignment[1])

    identical_positions = sum(1 for a, b in zip(aligned_seq1, aligned_seq2) if a == b and a != '-' and b != '-')
    total_positions = len([pos for pos in aligned_seq1 if pos != '-'])

    if total_positions == 0:
        return 0.0

    return (identical_positions / total_positions) * 100

def create_identity_matrix(sequences, labels):
    """
    Create a symmetric matrix of pairwise sequence identities.

    Args:
        sequences (list): List of protein sequences
        labels (list): List of sequence labels/names

    Returns:
        pd.DataFrame: Symmetric matrix with sequence identities
    """
    n = len(sequences)
    identity_matrix = np.zeros((n, n))

    # Fill diagonal with 100% identity
    np.fill_diagonal(identity_matrix, 100.0)

    # Calculate pairwise identities
    for i in range(n):
        for j in range(i + 1, n):
            identity = calculate_sequence_identity(sequences[i], sequences[j])
            identity_matrix[i, j] = identity
            identity_matrix[j, i] = identity  # Symmetric matrix

    return pd.DataFrame(identity_matrix, index=labels, columns=labels)

def plot_sequence_identity_heatmap(identity_df, title, output_file=None):
    """
    Create a heatmap of sequence identities similar to Figure 1b style.

    Args:
        identity_df (pd.DataFrame): Matrix of sequence identities
        title (str): Title for the plot
        output_file (str, optional): Path to save the plot
    """
    plt.figure(figsize=(5, 4.5))  # Even smaller figure for tiny squares

    # Create custom colormap from white to #0081A7
    custom_colors = ['#FFFFFF', '#0081A7']  # White to blue
    custom_cmap = LinearSegmentedColormap.from_list('custom_blue', custom_colors, N=256)

    # Create heatmap with custom styling
    mask = np.triu(np.ones_like(identity_df.values, dtype=bool), k=1)  # Mask upper triangle

    heatmap = sns.heatmap(
        identity_df,
        mask=mask,  # Show only lower triangle
        annot=True,
        fmt='.1f',
        cmap=custom_cmap,
        vmin=50,
        vmax=100,
        square=True,
        linewidths=0.2,  # Very thin lines for tiny squares
        cbar_kws={'label': 'Sequence Identity (%)', 'shrink': 0.7},
        annot_kws={'size': 10, 'color': 'white', 'weight': 'bold'}  # Smaller text to fit tiny squares
    )

    # Customize plot
    plt.title(title, fontsize=12, fontweight='bold', pad=10)
    plt.xlabel('MHCII Sequences', fontsize=8, fontweight='bold')
    plt.ylabel('MHCII Sequences', fontsize=8, fontweight='bold')

    # Rotate labels for better readability with smaller text
    plt.xticks(rotation=45, ha='right', fontsize=7)
    plt.yticks(rotation=0, fontsize=7)

    # Adjust layout
    plt.tight_layout()

    if output_file:
        plt.savefig(output_file, format='svg', bbox_inches='tight')
        print(f"Heatmap saved to: {output_file}")

    plt.show()

def main():
    """
    Main function to process MHCII data and create sequence identity heatmaps.
    """
    # Read the CSV file
    csv_path = "../../data/MHCII_genes.csv"

    try:
        df = pd.read_csv(csv_path)
        print(f"Loaded {len(df)} MHCII sequences from {csv_path}")
        print(f"Columns: {list(df.columns)}")
    except FileNotFoundError:
        print(f"Error: Could not find {csv_path}")
        return
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return

    # Extract sequences and labels
    labels = df['MHCII name'].tolist()
    alpha_sequences = df['alpha chain protein sequence'].tolist()
    beta_sequences = df['beta chain protein sequence'].tolist()

    print(f"\nProcessing {len(labels)} MHCII sequences:")
    for i, label in enumerate(labels):
        alpha_len = len(alpha_sequences[i]) if pd.notna(alpha_sequences[i]) else 0
        beta_len = len(beta_sequences[i]) if pd.notna(beta_sequences[i]) else 0
        print(f"  {label}: Alpha chain ({alpha_len} aa), Beta chain ({beta_len} aa)")

    # Create output directory
    os.makedirs("plots", exist_ok=True)

    # Calculate and plot alpha chain identities
    print("\nCalculating alpha chain sequence identities...")
    alpha_identity_df = create_identity_matrix(alpha_sequences, labels)

    print("Alpha chain identity matrix:")
    print(alpha_identity_df.round(1))

    plot_sequence_identity_heatmap(
        alpha_identity_df,
        "MHCII Alpha Chain Sequence Identity",
        "plots/mhcii_alpha_chain_identity_heatmap.svg"
    )

    # Calculate and plot beta chain identities
    print("\nCalculating beta chain sequence identities...")
    beta_identity_df = create_identity_matrix(beta_sequences, labels)

    print("Beta chain identity matrix:")
    print(beta_identity_df.round(1))

    plot_sequence_identity_heatmap(
        beta_identity_df,
        "MHCII Beta Chain Sequence Identity",
        "plots/mhcii_beta_chain_identity_heatmap.svg"
    )

    # Save identity matrices to CSV
    alpha_identity_df.round(1).to_csv("plots/alpha_chain_identity_matrix.csv")
    beta_identity_df.round(1).to_csv("plots/beta_chain_identity_matrix.csv")

    print(f"\nResults saved to:")
    print(f"  - Alpha chain heatmap: plots/mhcii_alpha_chain_identity_heatmap.svg")
    print(f"  - Beta chain heatmap: plots/mhcii_beta_chain_identity_heatmap.svg")
    print(f"  - Alpha identity matrix: plots/alpha_chain_identity_matrix.csv")
    print(f"  - Beta identity matrix: plots/beta_chain_identity_matrix.csv")

    # Summary statistics
    print(f"\nSummary Statistics:")

    # Alpha chain summary
    alpha_values = alpha_identity_df.values
    alpha_off_diagonal = alpha_values[np.triu_indices_from(alpha_values, k=1)]
    print(f"Alpha chain identities (excluding self-comparisons):")
    print(f"  Mean: {np.mean(alpha_off_diagonal):.1f}%")
    print(f"  Range: {np.min(alpha_off_diagonal):.1f}% - {np.max(alpha_off_diagonal):.1f}%")

    # Beta chain summary
    beta_values = beta_identity_df.values
    beta_off_diagonal = beta_values[np.triu_indices_from(beta_values, k=1)]
    print(f"Beta chain identities (excluding self-comparisons):")
    print(f"  Mean: {np.mean(beta_off_diagonal):.1f}%")
    print(f"  Range: {np.min(beta_off_diagonal):.1f}% - {np.max(beta_off_diagonal):.1f}%")

if __name__ == "__main__":
    main()