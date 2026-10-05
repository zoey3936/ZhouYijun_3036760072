# 01_explore.py
# 第一步：读取数据，认识数据，做出 Table 2 的描述统计

import pandas as pd

# 读取数据
df = pd.read_csv("data/raw/public.csv")
print(f"数据行数: {df.shape[0]}, 列数: {df.shape[1]}")

# ---- 构造核心变量 FTE（全时当量员工数）----
# 论文的算法：FTE = 全职员工 + 经理 + 0.5 × 兼职员工
df["FTE"] = df["EMPFT"] + df["NMGRS"] + 0.5 * df["EMPPT"]
df["FTE2"] = df["EMPFT2"] + df["NMGRS2"] + 0.5 * df["EMPPT2"]

# 政策后只有"成功回访"的店才有有效数据（STATUS2==1 表示回答了问卷）
print("\n政策后门店状态分布：")
print(df["STATUS2"].value_counts())

# 只看政策后回答了的店（暂时先这样处理）
answered = df[df["STATUS2"] == 1].copy()
print(f"\n政策后成功回访的店数: {len(answered)}")

# ---- Table 2 风格描述统计：NJ vs PA × 政策前 vs 政策后 ----
print("\n===== FTE 均值 =====")
print(answered.groupby("STATE")[["FTE", "FTE2"]].mean())

print("\n===== 起始工资均值 =====")
print(answered.groupby("STATE")[["WAGE_ST", "WAGE_ST2"]].mean())

# STATE: 1 = 新泽西(处理组), 0 = 宾州(对照组)
nj = answered[answered["STATE"] == 1]
pa = answered[answered["STATE"] == 0]

did_emp = (nj["FTE2"].mean() - nj["FTE"].mean()) - (pa["FTE2"].mean() - pa["FTE"].mean())
did_wage = (nj["WAGE_ST2"].mean() - nj["WAGE_ST"].mean()) - (pa["WAGE_ST2"].mean() - pa["WAGE_ST"].mean())

print(f"\n===== 简单 DiD 估计（手工算）=====")
print(f"就业 FTE 的 DiD: {did_emp:.3f}")
print(f"起始工资的 DiD: {did_wage:.3f}")