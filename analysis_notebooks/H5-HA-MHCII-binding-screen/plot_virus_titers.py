#!/usr/bin/env python3
"""
Script to process virus titer data from Excel files and create Altair plots.

This script processes H5 HA MHCII binding screen data by:
1. Reading raw RLU data from Excel files (96-well plate format)
2. Mapping virus IDs to strain names using plate layouts
3. Calculating RLU per µL values and aggregating replicates
4. Generating interactive Altair visualizations:
   - Faceted plot showing titers by strain (6 strains per row)
   - Combined plot with error bars and hover-activated trend lines
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

def get_color_scheme(config):
    """Extract color scheme from config and create color scale for Altair"""
    if 'colors' in config and config['colors']:
        # Convert the color mapping to the format Altair expects
        color_mapping = {}
        for color_entry in config['colors']:
            for cell_line, color_code in color_entry.items():
                color_mapping[cell_line] = color_code

        # Create domain (cell line names) and range (color codes) lists
        domain = list(color_mapping.keys())
        range_colors = list(color_mapping.values())

        return alt.Scale(domain=domain, range=range_colors)
    else:
        # Fallback to default color scheme if no colors specified
        CBPALETTE = ('#E69F00','#56B4E9','#999999','#009E73','#F0E442','#0072B2','#D55E00','#CC79A7')
        return alt.Scale(range=CBPALETTE)

def load_id_mapping(ids_path='data/IDs.csv'):
    """Load ID to strain, clade, and protein_sequence mapping"""
    ids_df = pd.read_csv(ids_path)
    # Clean up strain names (remove extra commas)
    ids_df['strain'] = ids_df['strain'].str.replace(',+$', '', regex=True)
    # Clean up clade names (remove extra spaces)
    ids_df['clade'] = ids_df['clade'].astype(str).str.strip()

    strain_mapping = dict(zip(ids_df['ID'], ids_df['strain']))
    clade_mapping = dict(zip(ids_df['ID'], ids_df['clade']))
    protein_sequence_mapping = dict(zip(ids_df['ID'], ids_df['protein_sequence']))

    return strain_mapping, clade_mapping, protein_sequence_mapping

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

def process_plate_data(excel_file, plate_layouts, strain_mapping, clade_mapping, protein_sequence_mapping, virus_volume):
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
                            'clade': clade_mapping[virus_id],
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
                      'clade': 'first',  # Keep clade for reference
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
                      'clade': 'first',
                      'protein_sequence': 'first'
                  })
                  .reset_index()
                 )

    # Flatten column names
    aggregated.columns = ['strain', 'cell_line', 'mean_RLUperuL', 'std_RLUperuL', 'count', 'ID', 'clade', 'protein_sequence']

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
                    'clade': row['clade'],
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
            'clade': row['clade'],
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

def create_titer_plot(data, virus_order=None, cell_order=None, color_scale=None):
    """Create Altair plot similar to the example"""

    # Use provided color scale or default
    if color_scale is None:
        CBPALETTE = ('#E69F00','#56B4E9','#999999','#009E73','#F0E442','#0072B2','#D55E00','#CC79A7')
        color_scale = alt.Scale(range=CBPALETTE)

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
            scale=alt.Scale(type="log", domain=[10, 1e8]),
            title="RLU per µL",
            axis=alt.Axis(
                titleFontSize=14,
                labelFontSize=12,
                format=".0e"
            ),
        ),
        color=alt.Color(
            "strain:N",
            scale=color_scale,
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
        size=300,
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

def extract_year_from_strain(strain_name):
    """Extract year from strain name, handling both 4-digit and 2-digit years"""
    import re

    # Look for 4-digit year (1900-2099) at the end of the strain name
    match_4digit = re.search(r'/(\d{4})$', strain_name)
    if match_4digit:
        return int(match_4digit.group(1))

    # Look for 2-digit year at the end, assume 1900s if >=50, 2000s if <50
    match_2digit = re.search(r'/(\d{2})$', strain_name)
    if match_2digit:
        year_2digit = int(match_2digit.group(1))
        if year_2digit >= 50:  # Assume 1950-1999
            return 1900 + year_2digit
        else:  # Assume 2000-2049
            return 2000 + year_2digit

    # If no year found, return a large number to sort at end
    return 9999

def create_virus_order_by_date_and_clade(data_with_errors):
    """Create virus order grouped by clade first, then by date within each clade group, with nonGsGd strains at the end"""
    # Get unique strain-clade combinations
    strain_clade = data_with_errors[['strain', 'clade']].drop_duplicates()

    # Extract year from strain names
    strain_clade['year'] = strain_clade['strain'].apply(extract_year_from_strain)

    # Create a sorting key for nonGsGd strains (put them at the end)
    strain_clade['is_nonGsGd'] = strain_clade['clade'].str.contains('nonGsGd', case=False, na=False)

    # Separate nonGsGd strains from regular strains
    regular_strains = strain_clade[~strain_clade['is_nonGsGd']].copy()
    nongsgd_strains = strain_clade[strain_clade['is_nonGsGd']].copy()

    # Sort regular strains by: clade first (primary grouping), then year within each clade, then strain name
    regular_sorted = regular_strains.sort_values(['clade', 'year', 'strain'])

    # Sort nonGsGd strains by: clade, then year, then strain name
    nongsgd_sorted = nongsgd_strains.sort_values(['clade', 'year', 'strain'])

    # Combine: regular strains first, then nonGsGd strains at the end
    final_order = pd.concat([regular_sorted, nongsgd_sorted], ignore_index=True)

    return final_order['strain'].tolist()

def create_virus_order_by_clade(data_with_errors):
    """Create virus order grouped by clade"""
    # Get unique strain-clade pairs
    strain_clade = data_with_errors[['strain', 'clade']].drop_duplicates()

    # Sort by clade first, then by strain name within each clade
    strain_clade_sorted = strain_clade.sort_values(['clade', 'strain'])

    return strain_clade_sorted['strain'].tolist()

def create_combined_titer_plot(data_with_errors, virus_order=None, cell_order=None, group_by_clade=True, title_suffix="", axis_domain=None, color_scale=None, width=None, height=None):
    """Create a combined plot similar to the flu-seqneut example with all data on one plot"""

    # Set default axis domain if not provided
    if axis_domain is None:
        axis_domain = [10, 1e8]

    # Use provided color scale or default
    if color_scale is None:
        CELL_COLORS = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f']
        color_scale = alt.Scale(range=CELL_COLORS)

    # Set default orders if not provided
    if virus_order is None:
        if group_by_clade:
            virus_order = create_virus_order_by_date_and_clade(data_with_errors)
        else:
            virus_order = sorted(data_with_errors['strain'].unique())

    if cell_order is None:
        cell_order = sorted(data_with_errors['cell_line'].unique())

    # Filter data to only include strains and cell lines in the orders
    data_filtered = data_with_errors[
        (data_with_errors['strain'].isin(virus_order)) &
        (data_with_errors['cell_line'].isin(cell_order))
    ].copy()

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

    # Create error bars
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
            scale=color_scale,
            legend=alt.Legend(
                title="Cell Line",
                orient="right",
                titleFontSize=13,
                labelFontSize=11,
                labelLimit=0,
                offset=80
            )
        ),
        tooltip=[
            alt.Tooltip('strain:N', title='Virus'),
            alt.Tooltip('clade:N', title='Clade'),
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
            scale=color_scale
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
            scale=color_scale,
            legend=alt.Legend(
                title="Cell Line",
                orient="right",
                titleFontSize=13,
                labelFontSize=11,
                labelLimit=0,
                offset=80
            )
        ),
        tooltip=[
            alt.Tooltip('strain:N', title='Virus'),
            alt.Tooltip('clade:N', title='Clade'),
            alt.Tooltip('cell_line:N', title='Cell Line'),
            alt.Tooltip('mean_RLUperuL:Q', format='.2e', title='Mean RLU/µL'),
            alt.Tooltip('sem_RLUperuL:Q', format='.2e', title='SEM'),
            alt.Tooltip('count:Q', title='Replicates')
        ]
    )

    # Add clade labels if grouping by clade
    chart_layers = [lines, error_bars, points]

    if group_by_clade:
        # Create clade labels for each strain (since clades can repeat across date groups)
        clade_labels_data = []

        for strain in virus_order:
            clade = data_filtered[data_filtered['strain'] == strain]['clade'].iloc[0]
            clade_labels_data.append({
                'clade': clade,
                'strain': strain,
                'label_x': 5  # Position at left side of chart
            })

        clade_labels_df = pd.DataFrame(clade_labels_data)

        # Add text labels for clades (one label per strain showing its clade)
        clade_text = alt.Chart(clade_labels_df).mark_text(
            align='left',
            baseline='middle',
            fontSize=10,
            fontWeight='bold',
            color='gray',
            dx=400  # Position clade labels even further left to avoid legend overlap
        ).encode(
            x=alt.value(10),  # Fixed x position
            y=alt.Y('strain:N', sort=virus_order),
            text='clade:N'
        )

        chart_layers.append(clade_text)

    # Combine all layers
    chart = (
        alt.layer(*chart_layers)
        .resolve_scale(
            color='independent'
        )
        .properties(
            width=width if width is not None else 600,
            height=height if height is not None else max(400, len(virus_order) * 12),  # Use custom height or dynamic height based on number of viruses
            title=alt.TitleParams(
                f"Virus Titers Across Cell Lines (Grouped by Clade){title_suffix}" if group_by_clade else f"Virus Titers Across Cell Lines with Error Bars{title_suffix}",
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

def create_fold_change_plot(fold_change_data, virus_order=None, cell_order=None, group_by_clade=True, title_suffix="", color_scale=None):
    """Create a fold-change plot showing titers relative to 293-noSA baseline"""

    # Use provided color scale or default
    if color_scale is None:
        CELL_COLORS = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f']
        color_scale = alt.Scale(range=CELL_COLORS)

    # Set default orders if not provided
    if virus_order is None:
        if group_by_clade:
            virus_order = create_virus_order_by_clade(fold_change_data)
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

    # Calculate axis domain based on actual data with padding
    min_fold_change = data_filtered['fold_change'].min()
    max_fold_change = data_filtered['fold_change'].max()

    # Add padding for log scale (multiply/divide by factor for better visualization)
    log_padding_factor = 1.2  # 20% padding in log space
    axis_min = min_fold_change / log_padding_factor
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

    # Create error bars
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
            scale=color_scale,
            legend=alt.Legend(
                title="Cell Line",
                orient="right",
                titleFontSize=13,
                labelFontSize=11,
                labelLimit=0,
                offset=80
            )
        ),
        tooltip=[
            alt.Tooltip('strain:N', title='Virus'),
            alt.Tooltip('clade:N', title='Clade'),
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
            scale=color_scale
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
            scale=alt.Scale(type='log', domain=[0.75, 15000]),
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
            scale=color_scale,
            legend=alt.Legend(
                title="Cell Line",
                orient="right",
                titleFontSize=13,
                labelFontSize=11,
                labelLimit=0,
                offset=80
            )
        ),
        tooltip=[
            alt.Tooltip('strain:N', title='Virus'),
            alt.Tooltip('clade:N', title='Clade'),
            alt.Tooltip('cell_line:N', title='Cell Line'),
            alt.Tooltip('fold_change:Q', format='.2f', title='Fold Change vs 293-noSA'),
            alt.Tooltip('fold_change_sem:Q', format='.2f', title='Fold Change SEM'),
            alt.Tooltip('test_titer:Q', format='.0f', title='Test Titer (RLU/µL)'),
            alt.Tooltip('baseline_titer:Q', format='.0f', title='293-noSA Titer (RLU/µL)'),
            alt.Tooltip('count:Q', title='Replicates')
        ]
    )

    # Add clade labels if grouping by clade
    chart_layers = [lines, error_bars, points]

    if group_by_clade:
        # Create clade labels for each strain (since clades can repeat across date groups)
        clade_labels_data = []

        for strain in virus_order:
            clade = data_filtered[data_filtered['strain'] == strain]['clade'].iloc[0]
            clade_labels_data.append({
                'clade': clade,
                'strain': strain,
                'label_x': 5  # Position at left side of chart
            })

        clade_labels_df = pd.DataFrame(clade_labels_data)

        # Add text labels for clades (one label per strain showing its clade)
        clade_text = alt.Chart(clade_labels_df).mark_text(
            align='left',
            baseline='middle',
            fontSize=10,
            fontWeight='bold',
            color='gray',
            dx=400  # Position clade labels even further left to avoid legend overlap
        ).encode(
            x=alt.value(10),  # Fixed x position
            y=alt.Y('strain:N', sort=virus_order),
            text='clade:N'
        )

        chart_layers.append(clade_text)

    # Combine all layers
    chart = (
        alt.layer(*chart_layers)
        .resolve_scale(
            color='independent'
        )
        .properties(
            width=400,   # Half A4 width (~105mm at 96 DPI)
            height=1120, # Full A4 height (~297mm at 96 DPI)
            title=alt.TitleParams(
                f"Fold Change vs 293-noSA Control (Grouped by Clade){title_suffix}" if group_by_clade else f"Fold Change vs 293-noSA Control{title_suffix}",
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

def create_cell_line_scatter_plot(data_qc_pass, cell_order=None, color_scale=None):
    """Create a scatter plot with cell lines on x-axis and titers on y-axis, with median annotations"""

    # Use provided color scale or default
    if color_scale is None:
        CELL_COLORS = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f']
        color_scale = alt.Scale(range=CELL_COLORS)

    # Set default cell order if not provided
    if cell_order is None:
        cell_order = sorted(data_qc_pass['cell_line'].unique())

    # Filter data to only include cell lines in the order
    data_filtered = data_qc_pass[data_qc_pass['cell_line'].isin(cell_order)].copy()

    # Set categorical ordering for cell lines and add numeric position for jittering
    data_filtered["cell_line"] = data_filtered["cell_line"].astype(
        CategoricalDtype(categories=cell_order, ordered=True)
    )

    # Add numeric position for each cell line (0, 1, 2, ...)
    cell_line_to_pos = {cell: i for i, cell in enumerate(cell_order)}
    data_filtered['cell_line_pos'] = data_filtered['cell_line'].map(cell_line_to_pos)

    # Calculate median titer for each cell line
    median_data = data_filtered.groupby('cell_line')['mean_RLUperuL'].median().reset_index()
    median_data.columns = ['cell_line', 'median_titer']

    # Set categorical ordering for median data and add positions
    median_data["cell_line"] = median_data["cell_line"].astype(
        CategoricalDtype(categories=cell_order, ordered=True)
    )
    median_data['cell_line_pos'] = median_data['cell_line'].map(cell_line_to_pos)

    # Create hover selection for strain-based lines
    hover = alt.selection_point(fields=['strain'], on='mouseover', empty=False, clear='mouseout', nearest=False)

    # Create base chart with hover selection
    base = alt.Chart(data_filtered).add_selection(hover).transform_calculate(
        # Add random jitter for each point
        jittered_x="indexof(" + str(cell_order) + ", datum.cell_line) + (random() - 0.5) * 0.6"
    )

    # Create hover lines connecting same strain across cell lines
    lines = base.mark_line(
        strokeWidth=2
    ).encode(
        x=alt.X('jittered_x:Q', scale=alt.Scale(domain=[-0.5, len(cell_order) - 0.5])),
        y=alt.Y('mean_RLUperuL:Q', scale=alt.Scale(type='log')),
        color=alt.value('gray'),  # Gray lines for subtle connection
        opacity=alt.condition(hover, alt.value(0.7), alt.value(0.0)),  # Only visible on hover
        detail='strain:N'  # Group by strain to connect same virus across cell lines
    )

    # Create scatter points
    scatter = base.mark_circle(
        size=150,  # Increased from 100 to 150
        opacity=0.8,
        stroke='white',  # White outline for better visibility
        strokeWidth=1.5
    ).encode(
        x=alt.X(
            'jittered_x:Q',
            scale=alt.Scale(domain=[-0.5, len(cell_order) - 0.5]),
            axis=alt.Axis(
                labelAngle=-45,
                labelFontSize=10,
                titleFontSize=12,
                labelLimit=0,
                values=list(range(len(cell_order))),
                labelExpr=f"indexof({list(range(len(cell_order)))}, datum.value) >= 0 ? {repr(cell_order)}[datum.value] : ''",
                grid=False  # Remove vertical grid lines
            ),
            title="Cell Line"
        ),
        y=alt.Y(
            'mean_RLUperuL:Q',
            scale=alt.Scale(type='log'),
            axis=alt.Axis(
                format='.2e',
                labelFontSize=10,
                titleFontSize=12,
                grid=False  # Remove horizontal grid lines
            ),
            title="Virus Titer (RLU/µL)"
        ),
        color=alt.Color(
            'cell_line:N',
            sort=cell_order,
            scale=color_scale,
            legend=alt.Legend(
                title="Cell Line",
                orient="right",
                titleFontSize=13,
                labelFontSize=11,
                labelLimit=0
            )
        ),
        tooltip=[
            alt.Tooltip('strain:N', title='Virus Strain'),
            alt.Tooltip('clade:N', title='Clade'),
            alt.Tooltip('cell_line:N', title='Cell Line'),
            alt.Tooltip('mean_RLUperuL:Q', format='.2e', title='Mean RLU/µL'),
            alt.Tooltip('sem_RLUperuL:Q', format='.2e', title='SEM'),
            alt.Tooltip('count:Q', title='Replicates')
        ]
    )

    # Create median annotation text at the top of plot area
    median_text = alt.Chart(median_data).mark_text(
        align='center',
        baseline='top',
        fontSize=10,
        fontWeight='bold',
        dy=-2,  # Position slightly lower (changed from -5 to -2)
        color='black'
    ).encode(
        x=alt.X(
            'cell_line_pos:Q',
            scale=alt.Scale(domain=[-0.5, len(cell_order) - 0.5])
        ),
        y=alt.value(5),  # Fixed position higher at top (changed from 10 to 5)
        text=alt.Text('median_titer:Q', format='.1e')
    )

    # Create solid black horizontal median line markers
    median_markers = alt.Chart(median_data).transform_calculate(
        x_left='datum.cell_line_pos - 0.25',
        x_right='datum.cell_line_pos + 0.25'
    ).mark_rule(
        color='black',
        strokeWidth=3,
        opacity=0.8
    ).encode(
        x=alt.X('x_left:Q', scale=alt.Scale(domain=[-0.5, len(cell_order) - 0.5])),
        x2=alt.X2('x_right:Q'),
        y=alt.Y('median_titer:Q', scale=alt.Scale(type='log'))
    )

    # Combine all components (lines behind points)
    chart = (lines + scatter + median_markers + median_text).resolve_scale(
        color='independent'
    ).properties(
        width=600,
        height=400,
        title=alt.TitleParams(
            text=["Cell Line Virus Titer Distribution (QC Pass Only)", "Black lines and labels show median titers. Hover over points to see strain connections."],
            fontSize=16,
            anchor='start'
        )
    )

    return chart

def create_fold_change_scatter_plot(fold_change_data, cell_order=None, color_scale=None):
    """Create a scatter plot with cell lines on x-axis and fold changes on y-axis, with median annotations"""

    # Use provided color scale or default
    if color_scale is None:
        CELL_COLORS = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f']
        color_scale = alt.Scale(range=CELL_COLORS)

    # Set default cell order if not provided (exclude 293-noSA since it's the baseline)
    if cell_order is None:
        cell_order = sorted([cl for cl in fold_change_data['cell_line'].unique() if cl != '293-noSA'])

    # Filter data to only include cell lines in the order
    data_filtered = fold_change_data[fold_change_data['cell_line'].isin(cell_order)].copy()

    # Set categorical ordering for cell lines and add numeric position for jittering
    data_filtered["cell_line"] = data_filtered["cell_line"].astype(
        CategoricalDtype(categories=cell_order, ordered=True)
    )

    # Add numeric position for each cell line (0, 1, 2, ...)
    cell_line_to_pos = {cell: i for i, cell in enumerate(cell_order)}
    data_filtered['cell_line_pos'] = data_filtered['cell_line'].map(cell_line_to_pos)

    # Calculate median fold change for each cell line
    median_data = data_filtered.groupby('cell_line')['fold_change'].median().reset_index()
    median_data.columns = ['cell_line', 'median_fold_change']

    # Set categorical ordering for median data and add positions
    median_data["cell_line"] = median_data["cell_line"].astype(
        CategoricalDtype(categories=cell_order, ordered=True)
    )
    median_data['cell_line_pos'] = median_data['cell_line'].map(cell_line_to_pos)

    # Create hover selection for strain-based lines
    hover = alt.selection_point(fields=['strain'], on='mouseover', empty=False, clear='mouseout', nearest=False)

    # Create base chart with hover selection
    base = alt.Chart(data_filtered).add_selection(hover).transform_calculate(
        # Add random jitter for each point
        jittered_x="indexof(" + str(cell_order) + ", datum.cell_line) + (random() - 0.5) * 0.6"
    )

    # Create hover lines connecting same strain across cell lines
    lines = base.mark_line(
        strokeWidth=2
    ).encode(
        x=alt.X('jittered_x:Q', scale=alt.Scale(domain=[-0.5, len(cell_order) - 0.5])),
        y=alt.Y('fold_change:Q', scale=alt.Scale(type='log')),
        color=alt.value('gray'),  # Gray lines for subtle connection
        opacity=alt.condition(hover, alt.value(0.7), alt.value(0.0)),  # Only visible on hover
        detail='strain:N'  # Group by strain to connect same virus across cell lines
    )

    # Create scatter points
    scatter = base.mark_circle(
        size=150,  # Same size as titer plot
        opacity=0.8,
        stroke='white',  # White outline for better visibility
        strokeWidth=1.5
    ).encode(
        x=alt.X(
            'jittered_x:Q',
            scale=alt.Scale(domain=[-0.5, len(cell_order) - 0.5]),
            axis=alt.Axis(
                labelAngle=-45,
                labelFontSize=10,
                titleFontSize=12,
                labelLimit=0,
                values=list(range(len(cell_order))),
                labelExpr=f"indexof({list(range(len(cell_order)))}, datum.value) >= 0 ? {repr(cell_order)}[datum.value] : ''",
                grid=False  # Remove vertical grid lines
            ),
            title="Cell Line"
        ),
        y=alt.Y(
            'fold_change:Q',
            scale=alt.Scale(type='log'),
            axis=alt.Axis(
                format='.2f',
                labelFontSize=10,
                titleFontSize=12,
                grid=False  # Remove horizontal grid lines
            ),
            title="Fold Change vs 293-noSA (log scale)"
        ),
        color=alt.Color(
            'cell_line:N',
            sort=cell_order,
            scale=color_scale,
            legend=alt.Legend(
                title="Cell Line",
                orient="right",
                titleFontSize=13,
                labelFontSize=11,
                labelLimit=0
            )
        ),
        tooltip=[
            alt.Tooltip('strain:N', title='Virus Strain'),
            alt.Tooltip('clade:N', title='Clade'),
            alt.Tooltip('cell_line:N', title='Cell Line'),
            alt.Tooltip('fold_change:Q', format='.2f', title='Fold Change'),
            alt.Tooltip('fold_change_sem:Q', format='.2f', title='Fold Change SEM'),
            alt.Tooltip('test_titer:Q', format='.0f', title='Test Titer (RLU/µL)'),
            alt.Tooltip('baseline_titer:Q', format='.0f', title='293-noSA Titer (RLU/µL)'),
            alt.Tooltip('count:Q', title='Replicates')
        ]
    )

    # Create median annotation text at the top of plot area
    median_text = alt.Chart(median_data).mark_text(
        align='center',
        baseline='top',
        fontSize=10,
        fontWeight='bold',
        dy=-2,  # Position slightly lower (changed from -5 to -2)
        color='black'
    ).encode(
        x=alt.X(
            'cell_line_pos:Q',
            scale=alt.Scale(domain=[-0.5, len(cell_order) - 0.5])
        ),
        y=alt.value(5),  # Fixed position higher at top
        text=alt.Text('median_fold_change:Q', format='.1f')
    )

    # Create solid black horizontal median line markers
    median_markers = alt.Chart(median_data).transform_calculate(
        x_left='datum.cell_line_pos - 0.25',
        x_right='datum.cell_line_pos + 0.25'
    ).mark_rule(
        color='black',
        strokeWidth=3,
        opacity=0.8
    ).encode(
        x=alt.X('x_left:Q', scale=alt.Scale(domain=[-0.5, len(cell_order) - 0.5])),
        x2=alt.X2('x_right:Q'),
        y=alt.Y('median_fold_change:Q', scale=alt.Scale(type='log'))
    )

    # Combine all components (lines behind points)
    chart = (lines + scatter + median_markers + median_text).resolve_scale(
        color='independent'
    ).properties(
        width=600,
        height=400,
        title=alt.TitleParams(
            text=["Cell Line Fold Change Distribution vs 293-noSA (QC Pass Only)", "Black lines and labels show median fold changes. Hover over points to see strain connections."],
            fontSize=16,
            anchor='start'
        )
    )

    return chart

def main():
    """Main function to process all data and create plots"""
    # Load configuration and mappings
    print("Loading configuration and mappings...")
    config = load_config()
    strain_mapping, clade_mapping, protein_sequence_mapping = load_id_mapping()
    plate_layouts = load_plate_layouts()

    virus_volume = config['virus_volume_ul']
    min_titers = config['min_titers']
    plates = config['plates']

    # Get custom color scheme
    color_scale = get_color_scheme(config)

    print(f"Loaded {len(strain_mapping)} virus strains, {len(plate_layouts)} plate layouts")
    print(f"Processing {len(plates)} plates with {virus_volume} µL virus volume")
    print(f"QC threshold: {min_titers} RLU/µL")

    # Process all Excel files
    all_data = []
    for plate in plates:
        excel_file = f"data/{plate}.xlsx"
        if os.path.exists(excel_file):
            plate_data = process_plate_data(excel_file, plate_layouts, strain_mapping, clade_mapping, protein_sequence_mapping, virus_volume)
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
    chart = create_titer_plot(aggregated_data, color_scale=color_scale)
    chart.save('results/virus_titers_processed.html')

    # Combined plot - all data
    combined_chart = create_combined_titer_plot(data_with_errors, group_by_clade=True, color_scale=color_scale)
    combined_chart.save('results/virus_titers_combined.html')

    # Combined plot - QC PASS only
    if len(data_pass) > 0:
        combined_chart_pass = create_combined_titer_plot(data_pass, group_by_clade=True, title_suffix=" - QC PASS", axis_domain=[100, 1e7], color_scale=color_scale, width=400, height=1120)
        combined_chart_pass.save('results/virus_titers_combined_QC_pass.html')
        print("Saved: results/virus_titers_combined_QC_pass.html")

        # Cell line scatter plot - QC PASS only
        cell_line_chart = create_cell_line_scatter_plot(data_pass, color_scale=color_scale)
        cell_line_chart.save('results/virus_titers_cell_line_scatter.html')
        print("Saved: results/virus_titers_cell_line_scatter.html")
    else:
        print("No viruses passed QC - skipping QC pass plot")

    # Combined plot - QC FAIL only
    if len(data_fail) > 0:
        combined_chart_fail = create_combined_titer_plot(data_fail, group_by_clade=True, title_suffix=" - QC FAIL", color_scale=color_scale)
        combined_chart_fail.save('results/virus_titers_combined_QC_fail.html')
        print("Saved: results/virus_titers_combined_QC_fail.html")
    else:
        print("No viruses failed QC - skipping QC fail plot")

    # Fold-change plot for QC pass viruses
    if fold_change_data is not None and len(fold_change_data) > 0:
        fold_change_chart = create_fold_change_plot(fold_change_data, group_by_clade=True, color_scale=color_scale)
        fold_change_chart.save('results/virus_titers_fold_change.html')
        print("Saved: results/virus_titers_fold_change.html")

        # Fold-change scatter plot - same style as cell line scatter
        fold_change_scatter_chart = create_fold_change_scatter_plot(fold_change_data, color_scale=color_scale)
        fold_change_scatter_chart.save('results/virus_titers_fold_change_scatter.html')
        print("Saved: results/virus_titers_fold_change_scatter.html")
    else:
        print("No fold-change data available - skipping fold-change plot")

    print("Saved: results/virus_titers_processed.html, results/virus_titers_combined.html")
    if len(data_pass) > 0:
        print("       results/virus_titers_cell_line_scatter.html")
    if fold_change_data is not None and len(fold_change_data) > 0:
        print("       results/virus_titers_fold_change_scatter.html")

    # Summary
    print(f"\n✓ Analysis complete:")
    print(f"  Total: {aggregated_data['strain'].nunique()} virus strains across {aggregated_data['cell_line'].nunique()} cell lines")
    print(f"  QC Pass: {len(passing_viruses)} viruses")
    print(f"  QC Fail: {len(failing_viruses)} viruses")

if __name__ == "__main__":
    main()