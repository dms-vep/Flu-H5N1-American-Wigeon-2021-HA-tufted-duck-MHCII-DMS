# ChimeraX Outputs

These notebooks create ChimeraX b-factor attribute files from binding and entry difference summary data.

## Project Structure

```
chimeraX_outputs/
├── plot_binding.ipynb              # Creates binding effect b-factors
├── plot_entry_difference.ipynb     # Creates entry difference b-factors  
├── bfactors_binding.defattr        # ChimeraX attribute file for binding (8.6KB)
├── bfactors_entry_difference.defattr # ChimeraX attribute file for entry (8.6KB)
└── README.md                       # This documentation
```

## Output Files

- **`bfactors_binding.defattr`**: ChimeraX attribute file mapping binding effects to B-factor column
- **`bfactors_entry_difference.defattr`**: ChimeraX attribute file for entry vs binding differences

## ChimeraX Attribute File Format

The generated `.defattr` files follow ChimeraX's standard format:

```
attribute: bfactor
match mode: 1-to-1
recipient: residues
	:1.A	-2.45
	:2.A	1.78
	:3.A	0.23
	...
```

## Usage

These notebooks need to be run manually.

```bash
jupyter notebook plot_binding.ipynb
jupyter notebook plot_entry_difference.ipynb
```

Load the resulting `.defattr` files in ChimeraX with:
```bash
open bfactors_binding.defattr
```