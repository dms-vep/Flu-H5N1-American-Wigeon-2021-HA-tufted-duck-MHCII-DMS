"""Custom rules used in the ``snakemake`` pipeline.

This file is included by the pipeline ``Snakefile``.

"""


rule nt_changes_to_codon:
    """Annotate how nucleotide changes to codon required for each amino-acid mutation."""
    input:
        natural_geneseq="data/American_Wigeon_H5N1_HA_EPI2709137.fa",
        site_numbering_map=config["site_numbering_map"],
        gene_sequence_protein=config["gene_sequence_protein"],
    output:
        annotations=config["mutation_annotations"],
    log:
        notebook="results/logs/nt_changes_to_codon.ipynb"
    conda:
        os.path.join(config["pipeline_path"], "environment.yml")
    notebook:
        "notebooks/nt_changes_to_codon.py.ipynb"

# Rules for comparing entry among cells -------------------------------------------------

# Some parameters for the comparison among cells
compare_entry_floor_mut_effects = -3  # before taking difference in cell entry, floor at this
# cells to compare
cells_to_compare = [
    "SA23 SA26 mix",
    "tufted duck MHCII",
    "SA23",
    "SA26",
]

rule cell_entry_mut_diffs:
    """Get CSV with differences in entry for mutations between cells after flooring."""
    input:
        mut_effects_csv="results/summaries/entry_all_cells.csv",
        nb="notebooks/cell_entry_mut_diffs.ipynb",
    output:
        mut_diffs_csv="results/compare_cell_entry/mut_diffs.csv",
        nb="results/notebooks/cell_entry_mut_diffs.ipynb",
    params:
        params_yaml=lambda wc: yaml_str(
            {
                # cells names in input CSV file
                "cells": cells_to_compare,
                # for calculating differences and display, floor mutation effects at this
                "floor_mut_effects": compare_entry_floor_mut_effects,
            }
        ),
    conda:
        os.path.join(config["pipeline_path"], "environment.yml"),
    log:
        "results/logs/cell_entry_mut_diffs.txt",
    shell:
        """
        papermill {input.nb} {output.nb} \
            -p mut_effects_csv {input.mut_effects_csv} \
            -p mut_diffs_csv {output.mut_diffs_csv} \
            -y "{params.params_yaml}" \
            &> {log}
        """


rule compare_cell_entry:
    """Compare entry across cell lines."""
    input:
        nb="notebooks/compare_cell_entry.ipynb",
        mut_effects_csv="results/summaries/entry_all_cells.csv",
    output:
        nb="results/notebooks/compare_cell_entry.ipynb",
        site_diffs_csv="results/compare_cell_entry/site_diffs.csv",
        mut_scatter_chart="results/compare_cell_entry/compare_cell_entry_scatter.html",
        site_zoom_chart="results/compare_cell_entry/compare_cell_entry_site_zoom.html",
    params:
        params_yaml=lambda wc: yaml_str(
            {
                # cells and their names in input CSV file
                "cells": dict(zip(cells_to_compare, cells_to_compare, strict=True)),
                # for calculating differences and display, floor mutation effects at this
                "floor_mut_effects": compare_entry_floor_mut_effects,
            }
        ),
    conda:
        os.path.join(config["pipeline_path"], "environment.yml"),
    log:
        "results/logs/compare_cell_entry.txt",
    shell:
        """
        papermill {input.nb} {output.nb} \
            -p mut_effects_csv {input.mut_effects_csv} \
            -p site_diffs_csv {output.site_diffs_csv} \
            -p mut_scatter_chart {output.mut_scatter_chart} \
            -p site_zoom_chart {output.site_zoom_chart} \
            -y "{params.params_yaml}" \
            &> {log}
        """


docs["Compare entry among cells"] = {
    "Final plots": {
        "Scatter plots of mutation effects in different cells": rules.compare_cell_entry.output.mut_scatter_chart,
        "Zoomable site chart of differences": rules.compare_cell_entry.output.site_zoom_chart,
    },
    "Analysis notebooks": {
        "Notebook making plots comparing entry": rules.compare_cell_entry.output.nb,
    },
    "Data files": {
        "site-differences in entry effects": rules.compare_cell_entry.output.site_diffs_csv,
        "mutation-differences in entry effects (after flooring negative values)":
            rules.cell_entry_mut_diffs.output.mut_diffs_csv,
    }
}

# Configure dmz-viz JSONs  -------------------------------------------------------------

# read configuration for `configure_dms_viz`
with open("data/dms_viz_config.yaml") as f:
    dms_viz_config = yaml.YAML(typ="safe", pure=True).load(f)

rule configure_dms_viz:
    """Configure a JSON for `dms-viz`."""
    input:
        data_csv=lambda wc: dms_viz_config[wc.viz_name]["data_csv"],
        sitemap_csv=lambda wc: dms_viz_config[wc.viz_name]["sitemap_csv"],
        nb="notebooks/configure_dms_viz.ipynb",
    output:
        dms_viz_json="results/dms-viz/{viz_name}/{viz_name}.json",
        pdb_file="results/dms-viz/{viz_name}/{viz_name}.pdb",
        input_data_csv="results/dms-viz/{viz_name}/{viz_name}_data.csv",
        input_sitemap_csv="results/dms-viz/{viz_name}/{viz_name}_sitemap.csv",
        nb="results/notebooks/configure_dms_viz_{viz_name}.ipynb",
    params:
        params_yaml=lambda wc: yaml_str(
            {
                key: dms_viz_config[wc.viz_name][key]
                for key in [
                    "pdb_id",
                    "pdb_type",
                    "name",
                    "melt_condition_metric_cols",
                    "metric",
                    "opt_params",
                ]
            }
        ),
    conda:
        "envs/dms-viz.yml"
    log:
        "results/logs/configure_dms_viz_{viz_name}.txt",
    shell:
        """
        papermill {input.nb} {output.nb} \
            -p data_csv {input.data_csv} \
            -p sitemap_csv {input.sitemap_csv} \
            -p dms_viz_json {output.dms_viz_json} \
            -p pdb_file {output.pdb_file} \
            -p input_data_csv {output.input_data_csv} \
            -p input_sitemap_csv {output.input_sitemap_csv} \
            -y "{params.params_yaml}" \
            &> {log}
        """

rule difference_binding_correlations:
    """Compare entry difference and MHCII binding."""
    input:
        nb="notebooks/compare_entry_difference_binding.ipynb",
        summary_df="results/summaries/tufted_duck_MHCII_binding.csv",
    output:
        nb="results/notebooks/compare_entry_difference_binding.ipynb",
        corr_chart="results/compare_cell_entry/corr_chart.html",
    conda:
        os.path.join(config["pipeline_path"], "environment.yml"),
    log:
        "results/logs/difference_binding_correlations.txt",
    shell:
        """
        papermill {input.nb} {output.nb} \
            -p summary_df {input.summary_df} \
            -p corr_chart {output.corr_chart} \
            &> {log}
        """

# Make row-wrapped heatmaps -------------------------------------------------------------

# read configuration for wrapped heatmaps
with open("data/wrapped_heatmap_config.yaml") as f:
    wrapped_heatmap_config = yaml.YAML(typ="safe", pure=True).load(f)


rule wrapped_heatmap:
    """Make row-wrapped heatmaps."""
    input:
        data_csv=lambda wc: wrapped_heatmap_config[wc.wrapped_hm]["data_csv"],
    output:
        chart_html="results/wrapped_heatmaps/{wrapped_hm}_wrapped_heatmap.html",
    params:
        params_dict=lambda wc: wrapped_heatmap_config[wc.wrapped_hm]
    log:
        notebook="results/notebooks/wrapped_heatmap_{wrapped_hm}.ipynb",
    conda:
        os.path.join(config["pipeline_path"], "environment.yml"),
    notebook:
        "notebooks/wrapped_heatmap.py.ipynb"

docs["Row-wrapped heatmaps"] = {
    "Heatmap HTMLs" : {
        wrapped_hm: rules.wrapped_heatmap.output.chart_html.format(wrapped_hm=wrapped_hm)
        for wrapped_hm in wrapped_heatmap_config
    }
}


docs["dms-viz visualizations"] = {
    "dms-viz JSON files": {
        viz_name: rules.configure_dms_viz.output.dms_viz_json.format(viz_name=viz_name)
        for viz_name in dms_viz_config
    },
    "Notebooks prepping dms-viz JSONs": {
        viz_name: rules.configure_dms_viz.output.nb.format(viz_name=viz_name)
        for viz_name in dms_viz_config
    },
}

docs["Additional files"] = {
    "HA site numbering": {
        "CSV converting among different protein numbering schemes":
            config["site_numbering_map"],
    },    
}

docs["Additional plots"] = {
    "Entry difference and MHCII binding correlations":
        rules.difference_binding_correlations.output.corr_chart   
}


# Add titer data to Appendix  -----------------------------------------------------------

docs["Entry titers measured for pseudoviruses with specific HAs from natural strains"] = {
    "Interactive charts" : {
        # H5
        "H5 HAs, titers normalized to noSA cells (horizontal)": "analysis_notebooks/strain_titers_with_trees/charts/H5_titer-relative-to-noSA_horizontal.html",
        "H5 HAs, titers normalized to noSA cells (vertical)": "analysis_notebooks/strain_titers_with_trees/charts/H5_titer-relative-to-noSA_vertical.html",
        "H5 HAs, raw titers (horizontal)": "analysis_notebooks/strain_titers_with_trees/charts/H5_raw-titer_horizontal.html",
        "H5 HAs, raw titers (vertical)": "analysis_notebooks/strain_titers_with_trees/charts/H5_raw-titer_vertical.html",
        # H1
        "H1 HAs, titers normalized to noSA cells (horizontal)": "analysis_notebooks/strain_titers_with_trees/charts/H1_titer-relative-to-noSA_horizontal.html",
        "H1 HAs, titers normalized to noSA cells (vertical)": "analysis_notebooks/strain_titers_with_trees/charts/H1_titer-relative-to-noSA_vertical.html",
        "H1 HAs, raw titers (horizontal)": "analysis_notebooks/strain_titers_with_trees/charts/H1_raw-titer_horizontal.html",
        "H1 HAs, raw titers (vertical)": "analysis_notebooks/strain_titers_with_trees/charts/H1_raw-titer_vertical.html",
        # H2
        "H2 HAs, titers normalized to noSA cells (horizontal)": "analysis_notebooks/strain_titers_with_trees/charts/H2_titer-relative-to-noSA_horizontal.html",
        "H2 HAs, titers normalized to noSA cells (vertical)": "analysis_notebooks/strain_titers_with_trees/charts/H2_titer-relative-to-noSA_vertical.html",
        "H2 HAs, raw titers (horizontal)": "analysis_notebooks/strain_titers_with_trees/charts/H2_raw-titer_horizontal.html",
        "H2 HAs, raw titers (vertical)": "analysis_notebooks/strain_titers_with_trees/charts/H2_raw-titer_vertical.html",
        # H3
        "H3 HAs, titers normalized to noSA cells (horizontal)": "analysis_notebooks/strain_titers_with_trees/charts/H3_titer-relative-to-noSA_horizontal.html",
        "H3 HAs, titers normalized to noSA cells (vertical)": "analysis_notebooks/strain_titers_with_trees/charts/H3_titer-relative-to-noSA_vertical.html",
        "H3 HAs, raw titers (horizontal)": "analysis_notebooks/strain_titers_with_trees/charts/H3_raw-titer_horizontal.html",
        "H3 HAs, raw titers (vertical)": "analysis_notebooks/strain_titers_with_trees/charts/H3_raw-titer_vertical.html",
    },
    "Numerical titers": {
        "H5 titers": "analysis_notebooks/H5-HA-MHCII-binding-screen/results/H5_pseudovirus_titer_summary.csv",
        "H1, H2, and H3 titers": "analysis_notebooks/H1_H2_H3_MHCII_entry_titers/results/pseudovirus_titer_summary.csv",
    },
}
