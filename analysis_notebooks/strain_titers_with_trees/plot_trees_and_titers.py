import marimo

__generated_with = "0.23.0"
app = marimo.App(width="full")


@app.cell
def _():
    # Setup with Python imports and tree config

    # All plot configuration goes in this cell

    import itertools
    import json
    import os

    import altair as alt

    import marimo as mo

    import pandas as pd

    import tree_annotated_plot

    chartsdir = "charts"
    os.makedirs(chartsdir, exist_ok=True)

    # Define the different plots to show; all plot configuration is done here.
    # Note paths to "tree" assume flu-ha-mhcii-usage-trees cloned in same root directory as this repo.
    plot_config = {
        "H5": {
            "titers": "../H5-HA-MHCII-binding-screen/results/virus_titer_QC_pass.csv",
            "titers_query": None,
            "tree": "../../../flu-ha-mhcii-usage-trees/auspice/flu-ha-mhcii-usage-trees_H5-with-titers.json",
            "titers_strain_renames": {
                "A/Hong_Kong/483/1997": "A/Hong Kong/483/1997",
                "A/Japanese_white-eye/Hong_Kong/1038/2006": "A/Japanese white-eye/Hong Kong/1038/2006",
                "A/common_magpie/Hong_Kong/5052/2007": "A/common magpie/Hong Kong/5052/2007",
            },
            "titers_shape": "square",
            "chart_step": 8,
            "kwargs": {
                "tree_size": 150,
                "strain_label_font_size": 7,
                "shift_tree_loc": 53,
                "branch_length": "div",
                "scale_bar": True,
                "branch_length_units": "substitutions per site",
                "scale_bar_font_size": 11,
            },
        },
        "H1": {
            "titers": "../H1_H2_H3_MHCII_entry_titers/results/virus_titer_QC_pass.csv",
            "titers_query": "subtype == 'H1'",
            "tree": "../../../flu-ha-mhcii-usage-trees/auspice/flu-ha-mhcii-usage-trees_H1-with-titers.json",
            "titers_strain_renames": {},
            "titers_strain_drops": ['A/WSN/1933-H141Y'],
            "titers_shape": "square",
            "chart_step": 13,
            "kwargs": {
                "tree_size": 150,
                "strain_label_font_size": 11,
                "shift_tree_loc": 54,
                "branch_length": "num_date",
                "scale_bar": True,
                "scale_bar_font_size": 11,
            },
        },
        "H3": {
            "titers": "../H1_H2_H3_MHCII_entry_titers/results/virus_titer_QC_pass.csv",
            "titers_query": "subtype == 'H3'",
            "tree": "../../../flu-ha-mhcii-usage-trees/auspice/flu-ha-mhcii-usage-trees_H3-with-titers.json",
            "titers_strain_renames": {},
            "titers_strain_drops": ['A/Netherlands/B1/1968'],
            "titers_shape": "square",
            "chart_step": 13,
            "kwargs": {
                "tree_size": 150,
                "strain_label_font_size": 11,
                "shift_tree_loc": 93,
                "branch_length": "num_date",
                "scale_bar": True,
                "scale_bar_font_size": 11,
            },
        },
        "H2": {
            "titers": "../H1_H2_H3_MHCII_entry_titers/results/virus_titer_QC_pass.csv",
            "titers_query": "subtype == 'H2'",
            "tree": "../../../flu-ha-mhcii-usage-trees/auspice/flu-ha-mhcii-usage-trees_H2-with-titers.json",
            "titers_strain_renames": {},
            "titers_shape": "square",
            "chart_step": 13,
            "kwargs": {
                "tree_size": 150,
                "strain_label_font_size": 11,
                "shift_tree_loc": 44,
                "branch_length": "num_date",
                "scale_bar": True,
                "scale_bar_font_size": 11,
            },
        },
    }

    # define colors used for different cell lines
    CELL_COLORS = {
        "noSA": '#989898',
        "SA23": '#2f6fb7',
        "SA26": '#6fb2ef',
        "noSA-tufted-duck-MHCII": '#c33d54',
        "noSA-human-MHCII-1503": "#0b6f50",
        "noSA-human-MHCII-0301": "#1eb684",
    }
    return (
        CELL_COLORS,
        alt,
        chartsdir,
        itertools,
        mo,
        os,
        pd,
        plot_config,
        tree_annotated_plot,
    )


@app.cell
def _(
    CELL_COLORS,
    alt,
    chartsdir,
    itertools,
    mo,
    os,
    pd,
    plot_config,
    tree_annotated_plot,
):
    # Make titer chart for each plot

    def make_titer_chart(titers_df, norm_to=None, vertical=True, chart_step=8, shape="circle"):
        df = (
            titers_df
            .rename(columns={"mean_RLUperuL": "titer"})
            [["strain", "cell_line", "titer", "upper_bound", "lower_bound"]]
            .assign(cell_line=lambda x: x["cell_line"].str.replace("293-", ""))
        )

        unknown = set(df["cell_line"]) - set(CELL_COLORS)
        if unknown:
            raise ValueError(
                f"cell_line values not in CELL_COLORS: {sorted(unknown)}"
            )
        domain = [c for c in CELL_COLORS if c in set(df["cell_line"])]
        color_range = [CELL_COLORS[c] for c in domain]
        if norm_to is not None:
            assert norm_to in set(df["cell_line"]), f"{norm_to}, {df['cell_line'].unique()}"
            df = (
                df
                .merge(
                    df[df["cell_line"] == norm_to]
                    [["strain", "titer"]]
                    .drop_duplicates()
                    .rename(columns={"titer": "norm"}),
                    on="strain",
                    validate="many_to_one",
                )
                .assign(
                    titer=lambda x: x["titer"] / x["norm"],
                    upper_bound=lambda x: x["upper_bound"] / x["norm"],
                    lower_bound=lambda x: x["lower_bound"] / x["norm"],
                )
                .drop(columns="norm")
            )
            assert len(df) == len(titers_df)

        titer_title = (
            f"titer relative to {norm_to} cells"
            if norm_to is not None
            else "raw titer (RLU/uL)"
        )
        titer_scale = alt.Scale(type="log", nice=False, padding=5)
        titer_axis = alt.Axis(tickCount=4, labelOverlap=True)

        if vertical:
            StrainCh, TiterCh, TiterCh2 = alt.Y, alt.X, alt.X2
            size_kwargs = {"height": alt.Step(chart_step), "width": 200}
        else:
            StrainCh, TiterCh, TiterCh2 = alt.X, alt.Y, alt.Y2
            size_kwargs = {"width": alt.Step(chart_step), "height": 200}

        legend_select = alt.selection_point(
            fields=["cell_line"],
            bind="legend",
            toggle="true",
            empty=False,
            value=[{"cell_line": c} for c in domain],
        )

        base = alt.Chart(df).encode(
            StrainCh(
                "strain",
                title=None,
                axis=alt.Axis(labelLimit=500, labelFontSize=8),
            ),
            alt.Color(
                "cell_line",
                title="293 cell line variant",
                scale=alt.Scale(range=color_range, domain=domain),
                legend=alt.Legend(orient="right", columns=1, symbolType=shape),
            ),
        )

        error_bars = base.mark_rule().encode(
            TiterCh("lower_bound", scale=titer_scale, axis=titer_axis, title=titer_title),
            TiterCh2("upper_bound"),
        )

        points_and_lines = (
            base
            .mark_line(strokeWidth=1.5, point=alt.OverlayMarkDef(size=chart_step * 4.5, shape=shape))
            .encode(
                TiterCh("titer", scale=titer_scale, axis=titer_axis, title=titer_title),
                tooltip=["strain", "cell_line", alt.Tooltip("titer", format=".3g")],
            )
        )

        chart = (
            (error_bars + points_and_lines)
            .add_params(legend_select)
            .transform_filter(legend_select)
            .properties(**size_kwargs)
        )

        return chart

    # loop over plots and make plots with normalized and raw titers in vertical and horizontal
    # orientations
    for name, config in plot_config.items():
        mo.output.append(mo.md(f"## Making plot for {name}"))
        titers = pd.read_csv(config["titers"]).assign(
            strain=lambda x: x["strain"].replace(config["titers_strain_renames"])
        )
        if config["titers_query"]:
            titers = titers.query(config["titers_query"])
        if "titers_strain_drops" in config:
            titers = titers[~titers["strain"].isin(config["titers_strain_drops"])]
        for norm_to, vertical in itertools.product([None, "noSA"], [True, False]):
            titer_chart = make_titer_chart(
                titers, norm_to=norm_to,
                vertical=vertical,
                chart_step=config["chart_step"],
                shape=config["titers_shape"],
            )
            tree_titer_chart = (
                tree_annotated_plot.plot(
                tree=config["tree"],
                chart=titer_chart,
                chart_strain_field="strain",
                tree_strain_field="strain",
                connect_leader_to_label=True,
                prune_tree_to_chart=True,
                **config["kwargs"],
                )
                .configure_legend(titleFontSize=14, labelFontSize=11, symbolLimit=50)
                .configure_axis(grid=False, titleFontSize=14)
            )
            mo.output.append(mo.md(f"### {name=}, {norm_to=}, {vertical=}"))
            chartfile = os.path.join(
                chartsdir,
                "_".join(
                    [
                        name,
                        f"titer-relative-to-{norm_to}" if norm_to else "raw-titer",
                        "vertical" if vertical else "horizontal"
                    ],
                )
            ) + ".html"
            mo.output.append(tree_titer_chart)
            mo.output.append(f"Saving above chart to {chartfile}")
            tree_titer_chart.save(chartfile)
    return (chartfile,)


@app.cell
def _(chartfile):
    chartfile
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
