# 05_extension.py
# 第五步（独立扩展）：低薪店 vs 高薪店——政策冲击强度检验

import pandas as pd
import statsmodels.formula.api as smf
import os

df = pd.read_csv("data/raw/public.csv")
df["FTE"] = df["EMPFT"] + df["NMGRS"] + 0.5 * df["EMPPT"]
d = df[df["STATUS2"] == 1].copy()
d["FTE2"] = d["EMPFT2"] + d["NMGRS2"] + 0.5 * d["EMPPT2"]

# 关键变量：政策前工资是否低于 5.05
d["LOW"] = (d["WAGE_ST"] < 5.05).astype(int)

print("各组店数（政策前工资口径）：")
print(d.groupby(["STATE", "LOW"]).size())

# 宽转长（带控制变量）
cols = ["STATE", "LOW", "CHAIN", "CO_OWNED", "FTE"]
db = d[cols].copy(); db["POST"] = 0; db = db.rename(columns={"FTE": "EMP"})
da = d[["STATE", "LOW", "CHAIN", "CO_OWNED", "FTE2"]].copy(); da["POST"] = 1; da = da.rename(columns={"FTE2": "EMP"})
long = pd.concat([db, da], ignore_index=True)
print(f"\n长格式数据行数: {len(long)}  (应该等于 399 × 2 = 798)")

# NJ 内部 DiD
nj = long[long.STATE == 1]
m_nj = smf.ols("EMP ~ LOW + POST + LOW:POST", data=nj).fit()
print("\n===== NJ 内部：低薪店 vs 高薪店 =====")
print(m_nj.summary().tables[1])

# 完整 DDD
m_ddd = smf.ols("EMP ~ STATE*POST*LOW", data=long).fit()
print("\n===== 三重差分（STATE×POST×LOW）=====")
print(m_ddd.summary().tables[1])

# 控制品牌和所有制的 DDD（新加的）
m_ddd_ctrl = smf.ols("EMP ~ STATE*POST*LOW + C(CHAIN) + CO_OWNED", data=long).fit()
print("\n===== 控制品牌和所有制的 DDD =====")
print(m_ddd_ctrl.summary().tables[1])

# 工资 DDD（验证处理强度）
wage_long = pd.concat([
    d[["STATE","LOW","WAGE_ST"]].rename(columns={"WAGE_ST":"WAGE"}).assign(POST=0),
    d[["STATE","LOW","WAGE_ST2"]].rename(columns={"WAGE_ST2":"WAGE"}).assign(POST=1)
], ignore_index=True)
m_wage = smf.ols("WAGE ~ STATE*POST*LOW", data=wage_long).fit()
print("\n===== 工资的三重差分 =====")
print(m_wage.summary().tables[1])

out = open("outputs/tables/extension.txt", "w", encoding="utf-8")
out.write("=== 扩展：低薪店 vs 高薪店 ===\n\n")
out.write("【NJ 内部 DiD】\n" + str(m_nj.summary().tables[1]) + "\n\n")
out.write("【三重差分 DDD】\n" + str(m_ddd.summary().tables[1]) + "\n\n")
out.write("【控制品牌和所有制的 DDD】\n" + str(m_ddd_ctrl.summary().tables[1]) + "\n\n")
out.write("【工资 DDD（验证处理强度）】\n" + str(m_wage.summary().tables[1]) + "\n")
out.close()
print("\n结果已写入 outputs/tables/extension.txt")