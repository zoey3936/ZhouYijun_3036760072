# Card & Krueger (1994) Replication and Extension
ECON6067 Individual Project

## Project structure
- `data/public.csv` — restaurant survey data (410 stores, two waves)
- `01_explore.py` — data loading and Table 2 descriptives
- `02_did.py` — baseline DiD regression (Table 3)
- `03_figure1.py` — Figure 1 bar chart
- `04_replication_rest.py` — full Table 2, sample composition, Table 4 robustness
- `05_extension.py` — independent extension (low-wage vs high-wage stores)
- `output/` — generated tables and figures

## How to reproduce
1. Place `public.csv` in `data/` (obtain from the course data package or
   Princeton's public replication archive for Card & Krueger 1994)
2. Run scripts in order: `python3 01_explore.py`, then `02_did.py`, ... , `05_extension.py`
3. Outputs are written to `output/`