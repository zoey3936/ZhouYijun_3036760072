# 03_figure1.py
# 第三步：画 Figure 1（FTE 均值柱状图）

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/raw/public.csv")
df["FTE"] = df["EMPFT"] + df["NMGRS"] + 0.5 * df["EMPPT"]
d = df[df["STATUS2"] == 1].copy()
d["FTE2"] = d["EMPFT2"] + d["NMGRS2"] + 0.5 * d["EMPPT2"]

means = d.groupby("STATE")[["FTE", "FTE2"]].mean()
# means 的行是 STATE（0=PA, 1=NJ），列是 FTE（政策前）、FTE2（政策后）

fig, ax = plt.subplots(figsize=(8, 6))
x = [0, 1]                        # 两组柱子的位置
width = 0.35                      # 柱子宽度

# PA（STATE=0）：政策前 / 政策后
ax.bar([i - width/2 for i in x], [means.loc[0, "FTE"], means.loc[1, "FTE"]],
       width, label="Before (Feb-Mar 1992)", color="steelblue")
# NJ（STATE=1）：政策前 / 政策后
ax.bar([i + width/2 for i in x], [means.loc[0, "FTE2"], means.loc[1, "FTE2"]],
       width, label="After (Nov-Dec 1992)", color="coral")

ax.set_xticks(x)
ax.set_xticklabels(["Pennsylvania", "New Jersey"])
ax.set_ylabel("Full-Time Equivalent Employment (FTE)")
ax.legend()

import os
os.makedirs("outputs/figures", exist_ok=True)
plt.savefig("outputs/figures/figure1.png", dpi=200, bbox_inches="tight")
print("图已保存到 outputs/figures/figure1.png")