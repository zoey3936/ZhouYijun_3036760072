# 02_did.py
# 第二步：用回归做 DiD（论文的标准做法）

import pandas as pd
import statsmodels.formula.api as smf

df = pd.read_csv("data/raw/public.csv")

# 构造 FTE（政策前）
df["FTE"] = df["EMPFT"] + df["NMGRS"] + 0.5 * df["EMPPT"]

# 只保留政策后回访成功的店
d = df[df["STATUS2"] == 1].copy()

# 构造政策后的 FTE 和"政策后"虚拟变量
d["FTE2"] = d["EMPFT2"] + d["NMGRS2"] + 0.5 * d["EMPPT2"]

# ---- 关键技巧：把数据变成"长格式"（每家店两行：政策前一行、政策后一行）----
d_before = d[["STATE", "FTE"]].copy()
d_before["POST"] = 0
d_before = d_before.rename(columns={"FTE": "EMP"})

d_after = d[["STATE", "FTE2"]].copy()
d_after["POST"] = 1
d_after = d_after.rename(columns={"FTE2": "EMP"})

long = pd.concat([d_before, d_after], ignore_index=True)
print(f"长格式数据行数: {len(long)}  (应该等于 399 × 2 = 798)")

# ---- DiD 回归：EMP = a + b·NJ + c·POST + d·(NJ×POST) ----
# 系数 d 就是 DiD 估计值
model = smf.ols("EMP ~ STATE + POST + STATE:POST", data=long).fit()
print(model.summary())