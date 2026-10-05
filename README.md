# Card & Krueger (1994) Replication and Extension
ECON6067 Individual Project

## Project structure
- `data/raw/public.csv` — original survey data (410 stores, two waves)
- `data/processed/analysis_panel.csv` — long-format analysis panel (built by run_all.py)
- `code/run_all.py` — runs the whole pipeline; start here
- `code/01_explore.py` ... `05_extension.py` — pipeline steps
- `outputs/tables/` — generated tables
- `outputs/figures/` — generated figures
- `report.pdf` — final report
- `AI_USE_DISCLOSURE.md` — AI-use documentation
- `skills/SKILL.md` — reusable workflow description

## How to reproduce
1. Put `public.csv` in `data/raw/`
2. From the repository root run `python3 code/run_all.py`
3. Outputs are written to `outputs/`