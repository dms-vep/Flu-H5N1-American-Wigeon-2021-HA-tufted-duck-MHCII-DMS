#!/usr/bin/env python3

"""
Create correlation plots with colored dots (blue for RBS sites, black for others) and no background lines.
"""

import pandas as pd
import altair as alt
import numpy as np
from scipy.stats import pearsonr
import yaml

# Load config
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Load the entry data
print("Loading entry data...")
df = pd.read_csv(config['entry_summary'])
print(f"Loaded {len(df)} rows of data")

# Collect all RBS sites from config
rbs_sites = set()
for key, sites in config.items():
    if key.startswith('RBS_') and isinstance(sites, list):
        rbs_sites.update(sites)
print(f"RBS sites defined: {sorted(rbs_sites)}")

# Define the cell lines of interest
cell_lines = [
    'entry in SA23 cells',
    'entry in SA26 cells',
    'entry in SA23 SA26 mix cells',
    'entry in tufted duck MHCII cells'
]

# Convert site column to numeric, handling non-numeric values
df['site_numeric'] = pd.to_numeric(df['site'], errors='coerce')

# Create hover label column (wildtype+site+mutant)
df['variant_label'] = df['wildtype'].astype(str) + df['site'].astype(str) + df['mutant'].astype(str)

# Add numeric color coding (0 = black, 1 = blue)
def get_color_numeric(site_num):
    if pd.isna(site_num):
        return 0  # black for invalid sites
    if int(site_num) in rbs_sites:
        return 1  # blue
    else:
        return 0  # black

df['color_code'] = df['site_numeric'].apply(get_color_numeric)
df['site_type'] = df['site_numeric'].apply(lambda x: 'RBS site' if not pd.isna(x) and int(x) in rbs_sites else 'Other site')

print(f"Sample of site values: {df['site'].head(10).tolist()}")
print(f"Sample of color codes: {df['color_code'].head(10).tolist()}")
print(f"Sample of site types: {df['site_type'].head(10).tolist()}")

# Check which RBS sites are actually in the data
rbs_sites_in_data = set(df[df['color_code'] == 1]['site_numeric'].dropna().astype(int).unique())
print(f"RBS sites found in data: {sorted(rbs_sites_in_data)}")
print(f"Total variants with RBS sites: {(df['color_code'] == 1).sum()}")

# Remove rows with any missing values in the cell lines of interest
df_clean = df.dropna(subset=cell_lines)
print(f"After removing rows with missing values: {len(df_clean)} rows")
print(f"RBS variants after cleaning: {(df_clean['color_code'] == 1).sum()}")

def create_correlation_plot(data, x_col, y_col, width=280, height=280):
    """Create a scatter plot with Pearson correlation coefficient."""

    # Calculate Pearson correlation
    corr_coef, p_value = pearsonr(data[x_col], data[y_col])

    # Create the base scatter plot with colored dots (blue for RBS sites, black for others)
    scatter = alt.Chart(data).mark_circle(
        size=40,
        opacity=0.3
    ).encode(
        x=alt.X(f'{x_col}:Q',
               title=x_col.replace('entry in ', '').replace(' cells', ''),
               axis=alt.Axis(grid=False)),
        y=alt.Y(f'{y_col}:Q',
               title=y_col.replace('entry in ', '').replace(' cells', ''),
               axis=alt.Axis(grid=False)),
        color=alt.Color('color_code:O',
                       scale=alt.Scale(domain=[0, 1],
                                     range=['black', '#4a90e2']),
                       legend=None),
        tooltip=[
            alt.Tooltip('variant_label:N', title='Variant'),
            alt.Tooltip('site:Q', title='Site'),
            alt.Tooltip('site_type:N', title='Site Type'),
            alt.Tooltip(f'{x_col}:Q', title=f'{x_col.replace("entry in ", "").replace(" cells", "")} titer', format='.3f'),
            alt.Tooltip(f'{y_col}:Q', title=f'{y_col.replace("entry in ", "").replace(" cells", "")} titer', format='.3f')
        ]
    ).properties(
        width=width,
        height=height
    )

    # Add correlation text
    corr_text = alt.Chart(pd.DataFrame([{
        'x': data[x_col].max() - 0.05 * (data[x_col].max() - data[x_col].min()),
        'y': data[y_col].min() + 0.05 * (data[y_col].max() - data[y_col].min()),
        'text': f'r = {corr_coef:.3f}'
    }])).mark_text(
        align='right',
        baseline='bottom',
        fontSize=14,
        fontWeight='bold',
        color='black'
    ).encode(
        x=alt.X('x:Q'),
        y=alt.Y('y:Q'),
        text=alt.Text('text:N')
    )

    return (scatter + corr_text).properties(
        title=alt.TitleParams(
            text=f'{x_col.replace("entry in ", "").replace(" cells", "")} vs {y_col.replace("entry in ", "").replace(" cells", "")}',
            fontSize=14,
            anchor='start'
        )
    )

# Create pairwise correlation plots (upper triangle only)
plots = []
for i in range(len(cell_lines)):
    for j in range(i+1, len(cell_lines)):
        plot = create_correlation_plot(df_clean, cell_lines[i], cell_lines[j])
        plots.append(plot)

# Create a simple legend
legend_data = pd.DataFrame([
    {'color': 'black', 'label': 'Non-RBS sites'},
    {'color': '#4a90e2', 'label': 'RBS sites'}
])

legend = alt.Chart(legend_data).mark_circle(size=100).encode(
    x=alt.value(20),
    y=alt.Y('label:N', axis=alt.Axis(title=None, labels=True, ticks=False)),
    color=alt.Color('color:N', scale=alt.Scale(range=['black', '#4a90e2']), legend=None)
).properties(
    width=120,
    height=60,
    title="Site Types"
)

# Arrange plots in a grid (2x3 for 6 plots)
row1 = alt.hconcat(plots[0], plots[1], plots[2])
row2 = alt.hconcat(plots[3], plots[4], plots[5])
chart_grid = alt.vconcat(row1, row2)

# Combine with legend
final_chart = alt.hconcat(chart_grid, legend, spacing=30)

# Add overall title and configure clean appearance
final_chart = final_chart.properties(
    title=alt.TitleParams(
        text="Correlations between Pseudovirus Entry Titers on Different Cell Lines",
        fontSize=18,
        anchor='start',
        offset=20
    )
).configure_axis(
    grid=False  # Remove grid lines from all plots
).configure_view(
    stroke=None  # Remove plot borders
)

# Save the plot (HTML only)
print("Saving correlation plots with colored dots...")
final_chart.save('entry_correlation_plots.html')
print("Plots saved to: entry_correlation_plots.html")

# Print summary
print("\n=== Summary ===")
print(f"Created {len(plots)} correlation plots")
print(f"Data points per plot: {len(df_clean)}")
print("Features:")
print("- BRIGHT BLUE (#4a90e2) dots for RBS sites, BLACK dots for other sites")
print("- 30% transparency")
print("- NO background grid lines")
print("- Hover tooltips showing variant labels, site number, and RBS status")
print("- Pearson correlation coefficient on each plot")
print("- Manual legend showing site type color coding")
print(f"- {len(rbs_sites)} RBS sites defined in config: {sorted(rbs_sites)}")

print("\n=== Correlation Coefficients ===")
plot_names = [
    ("SA23", "SA26"),
    ("SA23", "SA23 SA26 mix"),
    ("SA23", "tufted duck MHCII"),
    ("SA26", "SA23 SA26 mix"),
    ("SA26", "tufted duck MHCII"),
    ("SA23 SA26 mix", "tufted duck MHCII")
]

for i, (name1, name2) in enumerate(plot_names):
    x_col = f'entry in {name1} cells'
    y_col = f'entry in {name2} cells'
    if 'mix' in x_col:
        x_col = x_col.replace(' cells', ' cells')
    if 'mix' in y_col:
        y_col = y_col.replace(' cells', ' cells')
    corr_coef, _ = pearsonr(df_clean[x_col], df_clean[y_col])
    print(f"{name1} vs {name2}: r = {corr_coef:.3f}")