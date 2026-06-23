#!/usr/bin/env python3
"""
Script to process virus titer data from Excel files and create Altair plots.

This script processes H1H2H3 HA MHCII binding screen data by:
1. Reading raw RLU data from Excel files (96-well plate format)
2. Mapping virus IDs to strain names, subtypes, hosts, and metadata using plate layouts
3. Calculating RLU per µL values and aggregating replicates
4. Generating interactive Altair visualizations:
   - Faceted plot showing titers by strain (6 strains per row)
   - Combined plot with error bars, subtype grouping, host shapes, and hover-activated trend lines
   - Fold-change plots relative to 293-noSA baseline
   - NOTE: Scatter plots have been removed/disabled
"""

import os
import warnings
import yaml
import numpy as np
import pandas as pd
import altair as alt
from pandas.api.types import CategoricalDtype

warnings.simplefilter('ignore')

def load_config(config_path='data/config.yaml'):
    """Load configuration file"""
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config

def load_id_mapping(ids_path='data/IDs.csv'):
    """Load ID to strain, subtype, host, Genbank, plasmid_log_no, and protein_sequence mapping"""
    ids_df = pd.read_csv(ids_path)
    # Clean up strain names (remove extra commas)
    ids_df['strain'] = ids_df['strain'].str.replace(',+$', '', regex=True)
    # Clean up subtype and host names (remove extra spaces)
    ids_df['subtype'] = ids_df['subtype'].astype(str).str.strip()
    ids_df['host'] = ids_df['host'].astype(str).str.strip()

    strain_mapping = dict(zip(ids_df['ID'], ids_df['strain']))
    subtype_mapping = dict(zip(ids_df['ID'], ids_df['subtype']))
    host_mapping = dict(zip(ids_df['ID'], ids_df['host']))
    genbank_mapping = dict(zip(ids_df['ID'], ids_df['Genbank']))
    plasmid_log_mapping = dict(zip(ids_df['ID'], ids_df['plasmid_log_no']))
    protein_sequence_mapping = dict(zip(ids_df['ID'], ids_df['protein_sequence']))

    return strain_mapping, subtype_mapping, host_mapping, genbank_mapping, plasmid_log_mapping, protein_sequence_mapping

def load_plate_layouts(layout_path='data/plate_layouts.csv'):
    """Load plate layout information"""
    # Read CSV without headers to avoid treating first line as headers
    layout_df = pd.read_csv(layout_path, header=None)

    layouts = {}
    current_plate = None

    for idx, row in layout_df.iterrows():
        # Check if this row defines a new plate
        if pd.notna(row.iloc[0]) and 'plate' in str(row.iloc[0]).lower():
            current_plate = row.iloc[0]
            layouts[current_plate] = {}
            continue

        # Process rows A-H for the current plate
        if current_plate and pd.notna(row.iloc[0]) and row.iloc[0] in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']:
            row_letter = row.iloc[0]
            layouts[current_plate][row_letter] = []
            for col_idx in range(1, 13):  # columns 1-12 (r1-r12)
                if col_idx < len(row) and pd.notna(row.iloc[col_idx]):
                    if str(row.iloc[col_idx]) != 'NA':
                        try:
                            layouts[current_plate][row_letter].append(int(row.iloc[col_idx]))
                        except (ValueError, TypeError):
                            layouts[current_plate][row_letter].append(None)
                    else:
                        layouts[current_plate][row_letter].append(None)
                else:
                    layouts[current_plate][row_letter].append(None)

    return layouts

def read_excel_data(file_path):
    """Read RLU data from Excel file (B11:M18 range)"""
    try:
        # Read the specific range B11:M18 which corresponds to 96-well plate
        df = pd.read_excel(file_path, sheet_name=0, header=None,
                          usecols="B:M", skiprows=10, nrows=8)
        return df.values
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

def process_plate_data(excel_file, plate_layouts, strain_mapping, subtype_mapping, host_mapping, genbank_mapping, plasmid_log_mapping, protein_sequence_mapping, virus_volume):
    """Process a single Excel file and extract titer data"""
    # Extract plate number and cell line from filename
    basename = os.path.splitext(os.path.basename(excel_file))[0]

    # Extract just the plate number (e.g., "plate1" from "plate1-293-noSA-tufted-duck-MHCII")
    plate_key = None
    if basename.startswith('plate'):
        # Find the first dash and extract everything before it
        first_dash = basename.find('-')
        if first_dash != -1:
            plate_key = basename[:first_dash]
        else:
            plate_key = basename

    if plate_key is None or plate_key not in plate_layouts:
        print(f"Could not determine plate layout for {excel_file}")
        print(f"  Extracted plate key: {plate_key}")
        print(f"  Available layouts: {list(plate_layouts.keys())}")
        return None

    # Extract cell line name (everything after the plate identifier)
    parts = basename.split('-', 1)
    if len(parts) < 2:
        print(f"Could not extract cell line from {excel_file}")
        return None

    cell_line = parts[1]

    # Read Excel data
    excel_data = read_excel_data(excel_file)
    if excel_data is None:
        return None

    # Get plate layout
    layout = plate_layouts[plate_key]

    # Extract data for each ID
    titer_data = []

    for row_idx, row_letter in enumerate(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']):
        if row_letter in layout:
            for col_idx, virus_id in enumerate(layout[row_letter]):
                if virus_id is not None and row_idx < excel_data.shape[0] and col_idx < excel_data.shape[1]:
                    rlu_value = excel_data[row_idx, col_idx]
                    if pd.notna(rlu_value) and virus_id in strain_mapping:
                        titer_data.append({
                            'ID': virus_id,
                            'strain': strain_mapping[virus_id],
                            'subtype': subtype_mapping[virus_id],
                            'host': host_mapping[virus_id],
                            'Genbank': genbank_mapping[virus_id],
                            'plasmid_log_no': plasmid_log_mapping[virus_id],
                            'protein_sequence': protein_sequence_mapping[virus_id],
                            'cell_line': cell_line,
                            'RLU': float(rlu_value),
                            'RLU_per_uL': float(rlu_value) / virus_volume,
                            'plate': plate_key,
                            'row': row_letter,
                            'col': col_idx + 1
                        })

    return pd.DataFrame(titer_data)

def aggregate_titer_data(all_data):
    """Aggregate RLU data by taking mean across replicates for each strain and cell line"""
    aggregated = (all_data
                  .groupby(['strain', 'cell_line'])
                  .agg({
                      'RLU': 'mean',
                      'RLU_per_uL': 'mean',
                      'ID': 'first',  # Keep ID for reference
                      'subtype': 'first',  # Keep subtype for reference
                      'host': 'first',  # Keep host for reference
                      'Genbank': 'first',  # Keep Genbank for reference
                      'plasmid_log_no': 'first',  # Keep plasmid_log_no for reference
                      'protein_sequence': 'first'  # Keep protein_sequence for reference
                  })
                  .reset_index()
                  .rename(columns={
                      'RLU': 'mean_RLU',
                      'RLU_per_uL': 'mean_RLUperuL'
                  })
                 )

    return aggregated

def aggregate_with_error_bars(all_data):
    """Aggregate data with error bars (standard error of the mean)"""
    aggregated = (all_data
                  .groupby(['strain', 'cell_line'])
                  .agg({
                      'RLU_per_uL': ['mean', 'std', 'count'],
                      'ID': 'first',
                      'subtype': 'first',
                      'host': 'first',
                      'Genbank': 'first',
                      'plasmid_log_no': 'first',
                      'protein_sequence': 'first'
                  })
                  .reset_index()
                 )

    # Flatten column names
    aggregated.columns = ['strain', 'cell_line', 'mean_RLUperuL', 'std_RLUperuL', 'count', 'ID', 'subtype', 'host', 'Genbank', 'plasmid_log_no', 'protein_sequence']

    # Calculate standard error of the mean
    aggregated['sem_RLUperuL'] = aggregated['std_RLUperuL'] / np.sqrt(aggregated['count'])

    # Calculate error bar bounds
    aggregated['lower_bound'] = aggregated['mean_RLUperuL'] - aggregated['sem_RLUperuL']
    aggregated['upper_bound'] = aggregated['mean_RLUperuL'] + aggregated['sem_RLUperuL']

    # Ensure bounds don't go below zero
    aggregated['lower_bound'] = np.maximum(aggregated['lower_bound'], 1)  # Use 1 as minimum for log scale

    return aggregated

def qc_filter_viruses(data_with_errors, min_titers):
    """Filter viruses based on minimum titer threshold.
    A virus passes QC if it has titers > min_titers in ANY cell line."""

    # Find max titer for each virus across all cell lines
    max_titers_per_virus = (data_with_errors
                           .groupby('strain')
                           .agg({'mean_RLUperuL': 'max'})
                           .reset_index())

    # Determine which viruses pass QC
    passing_viruses = max_titers_per_virus[
        max_titers_per_virus['mean_RLUperuL'] > min_titers
    ]['strain'].tolist()

    failing_viruses = max_titers_per_virus[
        max_titers_per_virus['mean_RLUperuL'] <= min_titers
    ]['strain'].tolist()

    # Split data into pass/fail groups
    data_pass = data_with_errors[data_with_errors['strain'].isin(passing_viruses)].copy()
    data_fail = data_with_errors[data_with_errors['strain'].isin(failing_viruses)].copy()

    return data_pass, data_fail, passing_viruses, failing_viruses

def calculate_fold_changes(data_with_errors, baseline_cell_line='293-noSA'):
    """Calculate fold-changes relative to baseline cell line (293-noSA)"""

    # Get baseline titers for each virus
    baseline_data = data_with_errors[data_with_errors['cell_line'] == baseline_cell_line].copy()
    baseline_titers = dict(zip(baseline_data['strain'], baseline_data['mean_RLUperuL']))

    # Calculate fold-changes for all cell lines
    fold_change_data = []

    for _, row in data_with_errors.iterrows():
        strain = row['strain']
        cell_line = row['cell_line']

        if cell_line == baseline_cell_line:
            # Skip baseline - we'll add it back as 1.0
            continue

        if strain in baseline_titers:
            baseline_titer = baseline_titers[strain]
            if baseline_titer > 0:  # Avoid division by zero
                fold_change = row['mean_RLUperuL'] / baseline_titer

                # Propagate error for fold change calculation
                # Using error propagation: σ_fc = fc * sqrt((σ_test/test)² + (σ_baseline/baseline)²)
                baseline_row = baseline_data[baseline_data['strain'] == strain].iloc[0]
                relative_error_test = row['sem_RLUperuL'] / row['mean_RLUperuL'] if row['mean_RLUperuL'] > 0 else 0
                relative_error_baseline = baseline_row['sem_RLUperuL'] / baseline_titer

                fold_change_sem = fold_change * np.sqrt(relative_error_test**2 + relative_error_baseline**2)

                fold_change_data.append({
                    'strain': strain,
                    'subtype': row['subtype'],
                    'host': row['host'],
                    'Genbank': row['Genbank'],
                    'plasmid_log_no': row['plasmid_log_no'],
                    'protein_sequence': row['protein_sequence'],
                    'cell_line': cell_line,
                    'fold_change': fold_change,
                    'fold_change_sem': fold_change_sem,
                    'lower_bound': max(fold_change - fold_change_sem, 0.01),  # Min value for log scale
                    'upper_bound': fold_change + fold_change_sem,
                    'baseline_titer': baseline_titer,
                    'test_titer': row['mean_RLUperuL'],
                    'count': row['count']
                })

    # Add baseline values (fold-change = 1.0)
    for _, row in baseline_data.iterrows():
        fold_change_data.append({
            'strain': row['strain'],
            'subtype': row['subtype'],
            'host': row['host'],
            'Genbank': row['Genbank'],
            'plasmid_log_no': row['plasmid_log_no'],
            'protein_sequence': row['protein_sequence'],
            'cell_line': baseline_cell_line,
            'fold_change': 1.0,
            'fold_change_sem': 0.0,  # No error for baseline
            'lower_bound': 1.0,
            'upper_bound': 1.0,
            'baseline_titer': row['mean_RLUperuL'],
            'test_titer': row['mean_RLUperuL'],
            'count': row['count']
        })

    return pd.DataFrame(fold_change_data)

def create_titer_plot(data, virus_order=None, cell_order=None):
    """Create Altair plot similar to the example"""

    # Define color palette
    CBPALETTE = ('#E69F00','#56B4E9','#999999','#009E73','#F0E442','#0072B2','#D55E00','#CC79A7')

    # Set default orders if not provided
    if virus_order is None:
        virus_order = sorted(data['strain'].unique())

    if cell_order is None:
        cell_order = sorted(data['cell_line'].unique())

    # Filter data to only include strains and cell lines in the orders
    data_filtered = data[
        (data['strain'].isin(virus_order)) &
        (data['cell_line'].isin(cell_order))
    ].copy()

    # Calculate axis domain - fixed minimum at 10, auto-scaled maximum
    max_titer = data_filtered['mean_RLUperuL'].max()

    # Add padding for log scale (multiply by factor for better visualization)
    import math
    log_padding_factor = 2.0
    axis_min = 10  # Fixed minimum
    axis_max = max_titer * log_padding_factor

    # Set categorical ordering
    data_filtered["strain"] = data_filtered["strain"].astype(
        CategoricalDtype(categories=virus_order, ordered=True)
    )

    data_filtered["cell_line"] = data_filtered["cell_line"].astype(
        CategoricalDtype(categories=cell_order, ordered=True)
    )

    # Create base chart
    base = alt.Chart(data_filtered).encode(
        x=alt.X(
            "cell_line:N",
            sort=cell_order,
            title=None,
            axis=alt.Axis(
                labelAngle=90,
                labelFontSize=14,
                labelLimit=0
            ),
        ),
        y=alt.Y(
            "mean_RLUperuL:Q",
            scale=alt.Scale(type="log", domain=[axis_min, axis_max]),
            title="RLU per µL",
            axis=alt.Axis(
                titleFontSize=14,
                labelFontSize=12,
                format=".0e"
            ),
        ),
        color=alt.Color(
            "strain:N",
            scale=alt.Scale(range=CBPALETTE),
            legend=alt.Legend(
                title="virus",
                orient="bottom",
                titleFontSize=13,
                labelFontSize=12,
                labelLimit=0
            ),
        ),
        tooltip=[
            "strain:N",
            "cell_line:N",
            alt.Tooltip("mean_RLUperuL:Q", format=".2e"),
        ],
    )

    # Create points
    points = base.mark_point(
        size=150,
        filled=True,
        opacity=0.9,
        stroke="black",
        strokeWidth=1,
    )

    # Create faceted chart using facet() with columns parameter for wrapping
    chart = (
        points
        .properties(
            width=120,
            height=140
        )
        .facet(
            alt.Facet("strain:N", sort=virus_order),
            columns=6  # This should wrap to new rows every 6 columns
        )
        .properties(
            title="virus titers on different cell lines"
        )
        .resolve_scale(
            x="shared",  # Share x-axis across all plots
            y="shared"   # Share y-axis across all plots
        )
        .configure_axis(
            grid=False
        )
        .configure_view(
            stroke=None
        )
        .configure_title(
            fontSize=16
        )
        .configure_facet(
            spacing=15  # Spacing between panels
        )
        .configure_header(
            titleFontSize=0,  # Hide title
            labelFontSize=16,
            labelOrient="top"
        )
    )

    return chart

def create_fold_change_titer_plot(fold_change_data, virus_order=None, cell_order=None):
    """Create Altair faceted plot for fold change data similar to titer plot"""

    # Define color palette
    CBPALETTE = ('#E69F00','#56B4E9','#999999','#009E73','#F0E442','#0072B2','#D55E00','#CC79A7')

    # Set default orders if not provided
    if virus_order is None:
        virus_order = sorted(fold_change_data['strain'].unique())

    if cell_order is None:
        cell_order = sorted(fold_change_data['cell_line'].unique())

    # Filter data to only include strains and cell lines in the orders
    data_filtered = fold_change_data[
        (fold_change_data['strain'].isin(virus_order)) &
        (fold_change_data['cell_line'].isin(cell_order))
    ].copy()

    # Calculate axis domain based on actual data with padding, including error bars
    min_fold_change = data_filtered['lower_bound'].min()
    max_fold_change = data_filtered['upper_bound'].max()

    # Add padding for log scale (multiply/divide by factor for better visualization)
    import math
    log_padding_factor = 2.0
    axis_min = max(min_fold_change / log_padding_factor, 0.01)  # Don't go below 0.01 for log scale
    axis_max = max_fold_change * log_padding_factor

    # Set categorical ordering
    data_filtered["strain"] = data_filtered["strain"].astype(
        CategoricalDtype(categories=virus_order, ordered=True)
    )

    data_filtered["cell_line"] = data_filtered["cell_line"].astype(
        CategoricalDtype(categories=cell_order, ordered=True)
    )

    # Create base chart
    base = alt.Chart(data_filtered).encode(
        x=alt.X(
            "cell_line:N",
            sort=cell_order,
            title=None,
            axis=alt.Axis(
                labelAngle=90,
                labelFontSize=14,
                labelLimit=0
            ),
        ),
        y=alt.Y(
            "fold_change:Q",
            scale=alt.Scale(type="log", domain=[axis_min, axis_max]),
            title="Fold Change vs 293-noSA",
            axis=alt.Axis(
                titleFontSize=14,
                labelFontSize=12,
                format=".2f"
            ),
        ),
        color=alt.Color(
            "strain:N",
            scale=alt.Scale(range=CBPALETTE),
            legend=alt.Legend(
                title="virus",
                orient="bottom",
                titleFontSize=13,
                labelFontSize=12,
                labelLimit=0
            ),
        ),
        tooltip=[
            "strain:N",
            "cell_line:N",
            alt.Tooltip("fold_change:Q", format=".2f"),
        ],
    )

    # Create points
    points = base.mark_point(
        size=150,
        filled=True,
        opacity=0.9,
        stroke="black",
        strokeWidth=1,
    )

    # Create faceted chart using facet() with columns parameter for wrapping
    chart = (
        points
        .properties(
            width=120,
            height=140
        )
        .facet(
            alt.Facet("strain:N", sort=virus_order),
            columns=6  # This should wrap to new rows every 6 columns
        )
        .properties(
            title="virus fold changes on different cell lines"
        )
        .resolve_scale(
            x="shared",  # Share x-axis across all plots
            y="shared"   # Share y-axis across all plots
        )
        .configure_axis(
            grid=False
        )
        .configure_view(
            stroke=None
        )
        .configure_title(
            fontSize=16
        )
        .configure_facet(
            spacing=15  # Spacing between panels
        )
        .configure_header(
            titleFontSize=0,  # Hide title
            labelFontSize=16,
            labelOrient="top"
        )
    )

    return chart

def create_virus_order_by_subtype(data_with_errors):
    """Create virus order grouped by subtype"""
    # Get unique strain-subtype pairs
    strain_subtype = data_with_errors[['strain', 'subtype']].drop_duplicates()

    # Sort by subtype first, then by strain name within each subtype
    strain_subtype_sorted = strain_subtype.sort_values(['subtype', 'strain'])

    return strain_subtype_sorted['strain'].tolist()

def create_combined_titer_plot(data_with_errors, virus_order=None, cell_order=None, group_by_subtype=True, title_suffix="", axis_domain=None):
    """Create a combined plot similar to the flu-seqneut example with all data on one plot"""

    # Set default orders if not provided
    if virus_order is None:
        if group_by_subtype:
            virus_order = create_virus_order_by_subtype(data_with_errors)
        else:
            virus_order = sorted(data_with_errors['strain'].unique())

    if cell_order is None:
        cell_order = sorted(data_with_errors['cell_line'].unique())

    # Filter data to only include strains and cell lines in the orders
    data_filtered = data_with_errors[
        (data_with_errors['strain'].isin(virus_order)) &
        (data_with_errors['cell_line'].isin(cell_order))
    ].copy()

    # Set default axis domain if not provided
    if axis_domain is None:
        # Calculate axis domain - fixed minimum at 10, auto-scaled maximum including error bars
        max_titer = data_filtered['upper_bound'].max()

        # Add padding for log scale (multiply by factor for better visualization)
        import math
        log_padding_factor = 2.0
        axis_domain = [10, max_titer * log_padding_factor]  # Fixed minimum at 10

    # Define custom color mapping for cell lines (using original hex colors)
    CELL_COLOR_MAP = {
        '293-noSA-human-MHCII-1503': '#d62728',  # red
        '293-noSA-tufted-duck-MHCII': '#9467bd',  # violet
        '293-SA23': '#1f77b4',  # blue
        '293-noSA': '#ff7f0e',  # orange
        '293-noSA-human-MHCII-0301': '#2ca02c',  # green
        '293-SA26': '#8c564b'  # brown
    }

    # Create color list based on cell_order
    CELL_COLORS = [CELL_COLOR_MAP.get(cell, '#999999') for cell in cell_order]

    # Set categorical ordering
    data_filtered["strain"] = data_filtered["strain"].astype(
        CategoricalDtype(categories=virus_order, ordered=True)
    )

    data_filtered["cell_line"] = data_filtered["cell_line"].astype(
        CategoricalDtype(categories=cell_order, ordered=True)
    )

    # Create hover selection using the working pattern
    hover = alt.selection_point(fields=['cell_line'], on='mouseover', empty=False, clear='mouseout', nearest=False)

    # Create base chart with hover selection
    base = alt.Chart(data_filtered).add_selection(hover)

    # Create error bars (just lines, no shapes)
    error_bars = base.mark_rule(
        opacity=0.6,
        strokeWidth=1.5
    ).encode(
        x=alt.X('lower_bound:Q', scale=alt.Scale(type='log', domain=axis_domain)),
        x2=alt.X2('upper_bound:Q'),
        y=alt.Y(
            'strain:N',
            sort=virus_order,
            axis=alt.Axis(
                labelFontSize=8,
                labelLimit=200,
                titleFontSize=12
            ),
            title="Virus Strain"
        ),
        color=alt.Color(
            'cell_line:N',
            sort=cell_order,
            scale=alt.Scale(range=CELL_COLORS[:len(cell_order)]),
            legend=None  # Hide legend for error bars to avoid duplication
        ),
        tooltip=[
            alt.Tooltip('strain:N', title='Virus'),
            alt.Tooltip('subtype:N', title='Subtype'),
            alt.Tooltip('host:N', title='Host'),
            alt.Tooltip('cell_line:N', title='Cell Line'),
            alt.Tooltip('mean_RLUperuL:Q', format='.2e', title='Mean RLU/µL'),
            alt.Tooltip('sem_RLUperuL:Q', format='.2e', title='SEM'),
            alt.Tooltip('count:Q', title='Replicates')
        ]
    )

    # Create lines using the working pattern
    lines = base.mark_line().encode(
        x=alt.X(
            'mean_RLUperuL:Q',
            scale=alt.Scale(type='log', domain=axis_domain)
        ),
        y=alt.Y(
            'strain:N',
            sort=virus_order
        ),
        color=alt.Color(
            'cell_line:N',
            sort=cell_order,
            scale=alt.Scale(range=CELL_COLORS[:len(cell_order)])
        ),
        detail='cell_line:N',
        opacity=alt.condition(hover, alt.value(0.8), alt.value(0.2)),
        strokeWidth=alt.condition(hover, alt.value(4), alt.value(0.5))
    )

    # Create points
    points = base.mark_point(
        size=80,
        filled=True,
        stroke='black',
        strokeWidth=0.5,
        opacity=0.8
    ).encode(
        x=alt.X(
            'mean_RLUperuL:Q',
            scale=alt.Scale(type='log', domain=axis_domain),
            axis=alt.Axis(
                format='.0e',
                labelFontSize=10,
                titleFontSize=12,
                grid=True,
                gridOpacity=0.3
            ),
            title="RLU per µL"
        ),
        y=alt.Y(
            'strain:N',
            sort=virus_order,
            axis=alt.Axis(
                labelFontSize=8,
                labelLimit=200,
                titleFontSize=12
            ),
            title="Virus Strain"
        ),
        color=alt.Color(
            'cell_line:N',
            sort=cell_order,
            scale=alt.Scale(range=CELL_COLORS[:len(cell_order)]),
            legend=alt.Legend(
                title="Cell Line",
                orient="right",
                titleFontSize=13,
                labelFontSize=11,
                labelLimit=0
            )
        ),
        shape=alt.Shape(
            'host:N',
            legend=alt.Legend(
                title="Host",
                orient="right",
                titleFontSize=13,
                labelFontSize=11
            )
        ),
        tooltip=[
            alt.Tooltip('strain:N', title='Virus'),
            alt.Tooltip('subtype:N', title='Subtype'),
            alt.Tooltip('host:N', title='Host'),
            alt.Tooltip('cell_line:N', title='Cell Line'),
            alt.Tooltip('mean_RLUperuL:Q', format='.2e', title='Mean RLU/µL'),
            alt.Tooltip('sem_RLUperuL:Q', format='.2e', title='SEM'),
            alt.Tooltip('count:Q', title='Replicates')
        ]
    )

    # Add subtype labels if grouping by subtype
    chart_layers = [lines, error_bars, points]

    if group_by_subtype:
        # Create subtype labels
        subtype_labels_data = []
        current_position = 0
        subtype_positions = {}

        for strain in virus_order:
            subtype = data_filtered[data_filtered['strain'] == strain]['subtype'].iloc[0]
            if subtype not in subtype_positions:
                subtype_positions[subtype] = current_position
            current_position += 1

        # Create a separate dataframe for subtype labels
        for subtype, position in subtype_positions.items():
            subtype_labels_data.append({
                'subtype': subtype,
                'strain': virus_order[position],  # Use first strain in subtype for positioning
                'label_x': 5  # Position at left side of chart
            })

        subtype_labels_df = pd.DataFrame(subtype_labels_data)

        # Add text labels for subtypes
        subtype_text = alt.Chart(subtype_labels_df).mark_text(
            align='left',
            baseline='middle',
            fontSize=10,
            fontWeight='bold',
            color='gray',
            dx=570  # Position subtype labels moved back another 10px
        ).encode(
            x=alt.value(10),  # Fixed x position
            y=alt.Y('strain:N', sort=virus_order),
            text='subtype:N'
        )

        chart_layers.append(subtype_text)

    # Combine all layers
    chart = (
        alt.layer(*chart_layers)
        .resolve_scale(
            color='independent'
        )
        .properties(
            width=600,
            height=max(400, len(virus_order) * 12),  # Dynamic height based on number of viruses
            title=alt.TitleParams(
                f"Virus Titers Across Cell Lines (Grouped by Subtype){title_suffix}" if group_by_subtype else f"Virus Titers Across Cell Lines with Error Bars{title_suffix}",
                fontSize=16,
                anchor='start'
            )
        )
        .configure_axis(
            grid=False
        )
        .configure_view(
            stroke=None
        )
    )

    return chart

def create_fold_change_plot(fold_change_data, virus_order=None, cell_order=None, group_by_subtype=True, title_suffix=""):
    """Create a fold-change plot showing titers relative to 293-noSA baseline"""

    # Define custom color mapping for cell lines (using original hex colors)
    CELL_COLOR_MAP = {
        '293-noSA-human-MHCII-1503': '#d62728',  # red
        '293-noSA-tufted-duck-MHCII': '#9467bd',  # violet
        '293-SA23': '#1f77b4',  # blue
        '293-noSA': '#ff7f0e',  # orange
        '293-noSA-human-MHCII-0301': '#2ca02c',  # green
        '293-SA26': '#8c564b'  # brown
    }

    # Create color list based on cell_order
    if cell_order is None:
        cell_order = sorted(fold_change_data['cell_line'].unique())

    CELL_COLORS = [CELL_COLOR_MAP.get(cell, '#999999') for cell in cell_order]

    # Set default orders if not provided
    if virus_order is None:
        if group_by_subtype:
            virus_order = create_virus_order_by_subtype(fold_change_data)
        else:
            virus_order = sorted(fold_change_data['strain'].unique())

    if cell_order is None:
        cell_order = sorted(fold_change_data['cell_line'].unique())

    # Filter data to only include strains and cell lines in the orders
    data_filtered = fold_change_data[
        (fold_change_data['strain'].isin(virus_order)) &
        (fold_change_data['cell_line'].isin(cell_order))
    ].copy()

    # Set categorical ordering
    data_filtered["strain"] = data_filtered["strain"].astype(
        CategoricalDtype(categories=virus_order, ordered=True)
    )

    data_filtered["cell_line"] = data_filtered["cell_line"].astype(
        CategoricalDtype(categories=cell_order, ordered=True)
    )

    # Calculate axis domain based on actual data with padding, including error bars
    min_fold_change = data_filtered['lower_bound'].min()
    max_fold_change = data_filtered['upper_bound'].max()

    # Add padding for log scale (multiply/divide by factor for better visualization)
    log_padding_factor = 2.0  # More conservative padding in log space
    axis_min = max(min_fold_change / log_padding_factor, 0.01)  # Don't go below 0.01 for log scale
    axis_max = max_fold_change * log_padding_factor

    # Generate appropriate tick values based on the range
    import math
    log_min = math.log10(axis_min)
    log_max = math.log10(axis_max)

    # Create tick values at reasonable intervals
    tick_values = []
    # Start from the appropriate power of 10
    start_power = math.floor(log_min)
    end_power = math.ceil(log_max)

    for power in range(start_power, end_power + 1):
        base_value = 10 ** power
        if axis_min <= base_value <= axis_max:
            tick_values.append(base_value)
        # Add intermediate values for better resolution
        for multiplier in [2, 5]:
            intermediate_value = base_value * multiplier
            if axis_min <= intermediate_value <= axis_max:
                tick_values.append(intermediate_value)

    tick_values.sort()

    # Create hover selection using the working pattern
    hover = alt.selection_point(fields=['cell_line'], on='mouseover', empty=False, clear='mouseout', nearest=False)

    # Create base chart with hover selection
    base = alt.Chart(data_filtered).add_selection(hover)

    # Create error bars (just lines, no shapes)
    error_bars = base.mark_rule(
        opacity=0.6,
        strokeWidth=1.5
    ).encode(
        x=alt.X('lower_bound:Q', scale=alt.Scale(type='log', domain=[axis_min, axis_max])),
        x2=alt.X2('upper_bound:Q'),
        y=alt.Y(
            'strain:N',
            sort=virus_order,
            axis=alt.Axis(
                labelFontSize=8,
                labelLimit=200,
                titleFontSize=12
            ),
            title="Virus Strain"
        ),
        color=alt.Color(
            'cell_line:N',
            sort=cell_order,
            scale=alt.Scale(range=CELL_COLORS[:len(cell_order)]),
            legend=None  # Hide legend for error bars to avoid duplication
        ),
        tooltip=[
            alt.Tooltip('strain:N', title='Virus'),
            alt.Tooltip('subtype:N', title='Subtype'),
            alt.Tooltip('host:N', title='Host'),
            alt.Tooltip('cell_line:N', title='Cell Line'),
            alt.Tooltip('fold_change:Q', format='.2f', title='Fold Change vs 293-noSA'),
            alt.Tooltip('fold_change_sem:Q', format='.2f', title='Fold Change SEM'),
            alt.Tooltip('test_titer:Q', format='.0f', title='Test Titer (RLU/µL)'),
            alt.Tooltip('baseline_titer:Q', format='.0f', title='293-noSA Titer (RLU/µL)'),
            alt.Tooltip('count:Q', title='Replicates')
        ]
    )

    # Create lines using the working pattern
    lines = base.mark_line().encode(
        x=alt.X(
            'fold_change:Q',
            scale=alt.Scale(type='log', domain=[axis_min, axis_max])
        ),
        y=alt.Y(
            'strain:N',
            sort=virus_order
        ),
        color=alt.Color(
            'cell_line:N',
            sort=cell_order,
            scale=alt.Scale(range=CELL_COLORS[:len(cell_order)])
        ),
        detail='cell_line:N',
        opacity=alt.condition(hover, alt.value(0.8), alt.value(0.2)),
        strokeWidth=alt.condition(hover, alt.value(4), alt.value(0.5))
    )

    # Create points
    points = base.mark_point(
        size=60,
        filled=True,
        stroke='black',
        strokeWidth=0.5,
        opacity=0.8
    ).encode(
        x=alt.X(
            'fold_change:Q',
            scale=alt.Scale(type='log', domain=[axis_min, axis_max]),
            axis=alt.Axis(
                format='.2f',
                labelFontSize=10,
                titleFontSize=12,
                grid=True,
                gridOpacity=0.3,
                values=tick_values
            ),
            title="Fold Change vs 293-noSA (log scale)"
        ),
        y=alt.Y(
            'strain:N',
            sort=virus_order,
            axis=alt.Axis(
                labelFontSize=8,
                labelLimit=200,
                titleFontSize=12
            ),
            title="Virus Strain"
        ),
        color=alt.Color(
            'cell_line:N',
            sort=cell_order,
            scale=alt.Scale(range=CELL_COLORS[:len(cell_order)]),
            legend=alt.Legend(
                title="Cell Line",
                orient="right",
                titleFontSize=13,
                labelFontSize=11,
                labelLimit=0,
                offset=50
            )
        ),
        shape=alt.Shape(
            'host:N',
            legend=alt.Legend(
                title="Host",
                orient="right",
                titleFontSize=13,
                labelFontSize=11,
                offset=50
            )
        ),
        tooltip=[
            alt.Tooltip('strain:N', title='Virus'),
            alt.Tooltip('subtype:N', title='Subtype'),
            alt.Tooltip('host:N', title='Host'),
            alt.Tooltip('cell_line:N', title='Cell Line'),
            alt.Tooltip('fold_change:Q', format='.2f', title='Fold Change vs 293-noSA'),
            alt.Tooltip('fold_change_sem:Q', format='.2f', title='Fold Change SEM'),
            alt.Tooltip('test_titer:Q', format='.0f', title='Test Titer (RLU/µL)'),
            alt.Tooltip('baseline_titer:Q', format='.0f', title='293-noSA Titer (RLU/µL)'),
            alt.Tooltip('count:Q', title='Replicates')
        ]
    )

    # Add subtype labels if grouping by subtype
    chart_layers = [lines, error_bars, points]

    if group_by_subtype:
        # Create subtype labels
        subtype_labels_data = []
        current_position = 0
        subtype_positions = {}

        for strain in virus_order:
            subtype = data_filtered[data_filtered['strain'] == strain]['subtype'].iloc[0]
            if subtype not in subtype_positions:
                subtype_positions[subtype] = current_position
            current_position += 1

        # Create a separate dataframe for subtype labels
        for subtype, position in subtype_positions.items():
            subtype_labels_data.append({
                'subtype': subtype,
                'strain': virus_order[position],  # Use first strain in subtype for positioning
                'label_x': 5  # Position at left side of chart
            })

        subtype_labels_df = pd.DataFrame(subtype_labels_data)

        # Add text labels for subtypes
        subtype_text = alt.Chart(subtype_labels_df).mark_text(
            align='left',
            baseline='middle',
            fontSize=10,
            fontWeight='bold',
            color='gray',
            dx=570  # Position subtype labels moved back another 10px
        ).encode(
            x=alt.value(10),  # Fixed x position
            y=alt.Y('strain:N', sort=virus_order),
            text='subtype:N'
        )

        chart_layers.append(subtype_text)

    # Combine all layers
    chart = (
        alt.layer(*chart_layers)
        .resolve_scale(
            color='independent'
        )
        .properties(
            width=600,
            height=max(400, len(virus_order) * 12),  # Dynamic height based on number of viruses
            title=alt.TitleParams(
                f"Fold Change vs 293-noSA Control (Grouped by Subtype){title_suffix}" if group_by_subtype else f"Fold Change vs 293-noSA Control{title_suffix}",
                fontSize=16,
                anchor='start'
            )
        )
        .configure_axis(
            grid=False
        )
        .configure_view(
            stroke=None
        )
    )

    return chart

# REMOVED: create_cellline_scatter_plot function - scatter plots disabled

def create_subtype_plots(aggregated_data, data_with_errors, data_pass, data_fail, fold_change_data, min_titers):
    """Create separate plots for each subtype"""

    # Get unique subtypes
    subtypes = sorted(data_with_errors['subtype'].unique())
    print(f"\nGenerating subtype-specific plots for: {', '.join(subtypes)}")

    for subtype in subtypes:
        print(f"\n--- Processing {subtype} subtype ---")

        # Filter data by subtype
        agg_subtype = aggregated_data[aggregated_data['subtype'] == subtype].copy()
        errors_subtype = data_with_errors[data_with_errors['subtype'] == subtype].copy()

        if len(agg_subtype) == 0:
            print(f"  No data for {subtype} - skipping")
            continue

        # QC filtering for this subtype
        pass_subtype = data_pass[data_pass['subtype'] == subtype].copy()
        fail_subtype = data_fail[data_fail['subtype'] == subtype].copy()

        # Fold-change data for this subtype
        fold_subtype = None
        if fold_change_data is not None:
            fold_subtype = fold_change_data[fold_change_data['subtype'] == subtype].copy()

        strain_count = errors_subtype['strain'].nunique()
        pass_count = pass_subtype['strain'].nunique() if len(pass_subtype) > 0 else 0
        fail_count = fail_subtype['strain'].nunique() if len(fail_subtype) > 0 else 0

        print(f"  {subtype}: {strain_count} strains total, {pass_count} QC pass, {fail_count} QC fail")

        # Create suffix for filenames
        suffix = f"_{subtype}"

        # 1. Faceted plot (6 viruses per row) - all data for this subtype
        if len(agg_subtype) > 0:
            chart = create_titer_plot(agg_subtype)
            chart.save(f'results/virus_titers_processed{suffix}.html')

        # 2. Combined plot - all data for this subtype
        if len(errors_subtype) > 0:
            combined_chart = create_combined_titer_plot(errors_subtype, group_by_subtype=False, title_suffix=f" - {subtype}")
            combined_chart.save(f'results/virus_titers_combined{suffix}.html')

        # 3. Combined plot - QC PASS only for this subtype
        if len(pass_subtype) > 0:
            combined_chart_pass = create_combined_titer_plot(pass_subtype, group_by_subtype=False, title_suffix=f" - {subtype} QC PASS")
            combined_chart_pass.save(f'results/virus_titers_combined_QC_pass{suffix}.html')

        # 4. Combined plot - QC FAIL only for this subtype
        if len(fail_subtype) > 0:
            combined_chart_fail = create_combined_titer_plot(fail_subtype, group_by_subtype=False, title_suffix=f" - {subtype} QC FAIL")
            combined_chart_fail.save(f'results/virus_titers_combined_QC_fail{suffix}.html')

        # 5. Fold-change plot for QC pass viruses of this subtype
        if fold_subtype is not None and len(fold_subtype) > 0:
            fold_change_chart = create_fold_change_plot(fold_subtype, group_by_subtype=False, title_suffix=f" - {subtype}")
            fold_change_chart.save(f'results/virus_titers_fold_change{suffix}.html')

            # Faceted fold-change plot for this subtype
            fold_change_faceted_chart = create_fold_change_titer_plot(fold_subtype)
            fold_change_faceted_chart.save(f'results/virus_fold_change_processed{suffix}.html')

        # REMOVED: Cell line scatterplots - scatter plots disabled

def main():
    """Main function to process all data and create plots"""
    # Load configuration and mappings
    print("Loading configuration and mappings...")
    config = load_config()
    strain_mapping, subtype_mapping, host_mapping, genbank_mapping, plasmid_log_mapping, protein_sequence_mapping = load_id_mapping()
    plate_layouts = load_plate_layouts()

    virus_volume = config['virus_volume_ul']
    min_titers = config['min_titers']
    plates = config['plates']

    # Handle strain exclusion
    exclude_strains = config.get('exclude_strains', [])
    if exclude_strains:
        print(f"Excluding {len(exclude_strains)} strains: {', '.join(exclude_strains)}")
        # Find IDs of strains to exclude
        exclude_ids = []
        for strain_id, strain_name in strain_mapping.items():
            if strain_name in exclude_strains:
                exclude_ids.append(strain_id)

        # Remove excluded strains from all mappings
        for exclude_id in exclude_ids:
            if exclude_id in strain_mapping:
                del strain_mapping[exclude_id]
            if exclude_id in subtype_mapping:
                del subtype_mapping[exclude_id]
            if exclude_id in host_mapping:
                del host_mapping[exclude_id]
            if exclude_id in genbank_mapping:
                del genbank_mapping[exclude_id]
            if exclude_id in plasmid_log_mapping:
                del plasmid_log_mapping[exclude_id]
            if exclude_id in protein_sequence_mapping:
                del protein_sequence_mapping[exclude_id]

        print(f"Excluded {len(exclude_ids)} strain IDs from analysis: {exclude_ids}")

    print(f"Loaded {len(strain_mapping)} virus strains, {len(plate_layouts)} plate layouts")
    print(f"Processing {len(plates)} plates with {virus_volume} µL virus volume")
    print(f"QC threshold: {min_titers} RLU/µL")

    # Process all Excel files
    all_data = []
    for plate in plates:
        excel_file = f"data/{plate}.xlsx"
        if os.path.exists(excel_file):
            plate_data = process_plate_data(excel_file, plate_layouts, strain_mapping, subtype_mapping, host_mapping, genbank_mapping, plasmid_log_mapping, protein_sequence_mapping, virus_volume)
            if plate_data is not None and len(plate_data) > 0:
                all_data.append(plate_data)
                print(f"  {excel_file}: {len(plate_data)} data points")
        else:
            print(f"  Warning: {excel_file} not found")

    if not all_data:
        print("Error: No data was processed successfully!")
        return

    # Combine and save data
    combined_data = pd.concat(all_data, ignore_index=True)
    print(f"\nTotal: {len(combined_data)} data points from {combined_data['strain'].nunique()} strains and {combined_data['cell_line'].nunique()} cell lines")

    # Create results directory if it doesn't exist
    os.makedirs('results', exist_ok=True)

    # Save outputs
    combined_data.to_csv('results/virus_titer_raw_data.csv', index=False)

    aggregated_data = aggregate_titer_data(combined_data)
    aggregated_data.to_csv('results/virus_titer_aggregated.csv', index=False)

    data_with_errors = aggregate_with_error_bars(combined_data)
    data_with_errors.to_csv('results/virus_titer_with_errors.csv', index=False)

    print("Saved: results/virus_titer_raw_data.csv, results/virus_titer_aggregated.csv, results/virus_titer_with_errors.csv")

    # Apply QC filtering
    print(f"\nApplying QC filter (min titer: {min_titers} RLU/µL)...")
    data_pass, data_fail, passing_viruses, failing_viruses = qc_filter_viruses(data_with_errors, min_titers)

    print(f"QC Results:")
    print(f"  ✓ PASS: {len(passing_viruses)} viruses (successfully rescued)")
    print(f"  ✗ FAIL: {len(failing_viruses)} viruses (rescue failed/low titers)")

    # Save QC results
    data_pass.to_csv('results/virus_titer_QC_pass.csv', index=False)
    data_fail.to_csv('results/virus_titer_QC_fail.csv', index=False)
    print("Saved: results/virus_titer_QC_pass.csv, results/virus_titer_QC_fail.csv")

    # Calculate fold-changes for QC pass viruses only
    if len(data_pass) > 0:
        print(f"\nCalculating fold-changes vs 293-noSA for {len(passing_viruses)} QC pass viruses...")
        fold_change_data = calculate_fold_changes(data_pass, baseline_cell_line='293-noSA')
        fold_change_data.to_csv('results/virus_titer_fold_changes.csv', index=False)
        print("Saved: results/virus_titer_fold_changes.csv")
    else:
        print("No viruses passed QC - skipping fold-change analysis")
        fold_change_data = None

    # Create plots
    print("\nGenerating visualizations...")

    # Faceted plot (6 viruses per row) - all data
    chart = create_titer_plot(aggregated_data)
    chart.save('results/virus_titers_processed.html')

    # Combined plot - all data
    combined_chart = create_combined_titer_plot(data_with_errors, group_by_subtype=True)
    combined_chart.save('results/virus_titers_combined.html')

    # Combined plot - QC PASS only
    if len(data_pass) > 0:
        combined_chart_pass = create_combined_titer_plot(data_pass, group_by_subtype=True, title_suffix=" - QC PASS")
        combined_chart_pass.save('results/virus_titers_combined_QC_pass.html')
        print("Saved: results/virus_titers_combined_QC_pass.html")
    else:
        print("No viruses passed QC - skipping QC pass plot")

    # Combined plot - QC FAIL only
    if len(data_fail) > 0:
        combined_chart_fail = create_combined_titer_plot(data_fail, group_by_subtype=True, title_suffix=" - QC FAIL")
        combined_chart_fail.save('results/virus_titers_combined_QC_fail.html')
        print("Saved: results/virus_titers_combined_QC_fail.html")
    else:
        print("No viruses failed QC - skipping QC fail plot")

    # Fold-change plot for QC pass viruses
    if fold_change_data is not None and len(fold_change_data) > 0:
        fold_change_chart = create_fold_change_plot(fold_change_data, group_by_subtype=True)
        fold_change_chart.save('results/virus_titers_fold_change.html')
        print("Saved: results/virus_titers_fold_change.html")

        # Faceted fold-change plot (6 viruses per row)
        fold_change_faceted_chart = create_fold_change_titer_plot(fold_change_data)
        fold_change_faceted_chart.save('results/virus_fold_change_processed.html')
        print("Saved: results/virus_fold_change_processed.html")
    else:
        print("No fold-change data available - skipping fold-change plot")

    # REMOVED: Cell line scatterplots - scatter plots disabled
    print("Scatterplots disabled - skipping scatter plot generation")

    print("Saved: results/virus_titers_processed.html, results/virus_titers_combined.html")

    # Create subtype-specific plots
    create_subtype_plots(aggregated_data, data_with_errors, data_pass, data_fail, fold_change_data, min_titers)

    # Summary
    print(f"\n✓ Analysis complete:")
    print(f"  Total: {aggregated_data['strain'].nunique()} virus strains across {aggregated_data['cell_line'].nunique()} cell lines")
    print(f"  QC Pass: {len(passing_viruses)} viruses")
    print(f"  QC Fail: {len(failing_viruses)} viruses")

if __name__ == "__main__":
    main()