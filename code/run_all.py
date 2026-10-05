# code/run_all.py
# Runs the full pipeline from raw data to all tables and figures.
# Usage (from the repository root):  python3 code/run_all.py

import os
import subprocess
import sys
from pathlib import Path

os.environ["MPLBACKEND"] = "Agg"  # save figures without opening windows

ROOT = Path(__file__).resolve().parent.parent

# ---- Step 0: build and save the processed analysis panel ----
import pandas as pd
df = pd.read_csv(ROOT / "data/raw/public.csv")
df["FTE"] = df["EMPFT"] + df["NMGRS"] + 0.5 * df["EMPPT"]
d = df[df["STATUS2"] == 1].copy()
d["FTE2"] = d["EMPFT2"] + d["NMGRS2"] + 0.5 * d["EMPPT2"]

before = d[["STATE", "FTE"]].rename(columns={"FTE": "EMP"}); before["POST"] = 0
after = d[["STATE", "FTE2"]].rename(columns={"FTE2": "EMP"}); after["POST"] = 1
panel = pd.concat([before, after], ignore_index=True)

(ROOT / "data/processed").mkdir(parents=True, exist_ok=True)
panel.to_csv(ROOT / "data/processed/analysis_panel.csv", index=False)
print("Processed panel saved to data/processed/analysis_panel.csv")

# ---- Steps 1-5: replication scripts ----
for s in ["01_explore.py", "02_did.py", "03_figure1.py",
          "04_replication_rest.py", "05_extension.py"]:
    print(f"\n===== Running code/{s} =====")
    subprocess.run([sys.executable, str(ROOT / "code" / s)], cwd=ROOT, check=True)

print("\nAll done. Tables -> outputs/tables/, figures -> outputs/figures/")