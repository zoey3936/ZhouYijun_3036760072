# Skill: Card & Krueger (1994) Replication Pipeline

Regenerates all main tables and figures of this project from the raw survey data.

## Inputs
- `data/raw/public.csv` — 410-store survey file (waves 1 and 2)

## How to run
From the repository root:
    python3 code/run_all.py

## Outputs
- `outputs/tables/tables.txt` — descriptive statistics, sample composition, robustness
- `outputs/tables/extension.txt` — extension regressions
- `outputs/figures/figure1.png` — FTE means bar chart

## Key definitions
- FTE = EMPFT + NMGRS + 0.5 * EMPPT (both waves)
- Sample: stores with STATUS2 == 1 (399 stores, balanced panel)
- Extension: LOW = 1 if pre-policy starting wage &lt; 5.05