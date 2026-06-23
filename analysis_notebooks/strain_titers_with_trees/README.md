# Plot titers of strains alongside phylogenetic trees
This subdirectory uses [altair](https://altair-viz.github.io/) and [tree-annotated-plot](https://jbloomlab.github.io/tree-annotated-plot/) to plot the relative titers of pseudoviruses with different HAs alongside a phylogenetic tree.

The titers are read from other subdirectories in this repo, and the trees are taken from [https://github.com/jbloomlab/flu-ha-mhcii-usage-trees/](https://github.com/jbloomlab/flu-ha-mhcii-usage-trees/).

To run, first build and activate an appropriate Python virtual environment, and install the necessary packages
(requires you to have Python 3.13 installed):
```bash
python3.13 -m venv .venv
source .venv/bin/activate
pip install tree-annotated-plot==0.2.2 marimo==0.23
```
Then for subsequent uses just activate this with:
```bash
source .venv/bin/activate
```

Then open and run the marimo notebook [plot_trees_and_titers.py](plot_trees_and_titers.py).

The charts produced by the notebook are saved as interative HTMLs nto [./charts](charts)
