# 05_extension.py
# 第五步（独立扩展）：低薪店 vs 高薪店——政策冲击强度检验

import pandas as pd
import statsmodels.formula.api as smf
import os

os.makedirs("outputs/tables", exist_ok=True)

df = pd.read_csv("data/raw/public.csv")
df["FTE"] = df["EMPFT"] + df["NMGRS"] + 0.5 * df["EMPPT"]
d = df[df["STATUS2"] == 1].copy()
d["FTE2"] = d["EMPFT2"] + d["NMGRS2"] + 0.5 * d["EMPPT2"]

# ---- 关键变量：政策前工资是否低于 5.05（新政策工资）----
# 1 = 低薪店（被政策约束，必须涨薪）；0 = 高薪店（本来就不受约束）
d["LOW"] = (d["WAGE_ST"] < 5.05).astype(int)

print("各组店数（政策前工资口径）：")
print(d.groupby(["STATE", "LOW"]).size())

# ---- 宽转长 ----
cols = ["STATE", "LOW", "FTE"]
db = d[cols].copy();              db["POST"] = 0; db = db.rename(columns={"FTE": "EMP"})
da = d[["STATE", "LOW", "FTE2"]].copy(); da["POST"] = 1; da = da.rename(columns={"FTE2": "EMP"})
long = pd.concat([db, da], ignore_index=True)

# ---- 扩展 1：先看 NJ 内部（高薪店作对照）----
nj = long[long.STATE == 1]
m_nj = smf.ols("EMP ~ LOW + POST + LOW:POST", data=nj).fit()
print("\n===== NJ 内部：低薪店 vs 高薪店（低薪店=处理组）=====")
print(m_nj.summary().tables[1])   # 只看系数表

# ---- 扩展 2：完整三重差分（用 PA 再剔除一层共同冲击，更严格）----
m_ddd = smf.ols("EMP ~ STATE*POST*LOW", data=long).fit()
print("\n===== 三重差分（STATE×POST×LOW）=====")
print(m_ddd.summary().tables[1])

# 解读重点：STATE:POST:LOW 的系数
# = 低薪店相对于高薪店的"额外"就业变化（NJ 减去 PA 之后）

# ---- 扩展 3：验证处理确实集中在低薪店（工资变化本身）----
m_wage = smf.ols("WAGE ~ STATE*POST*LOW", data=pd.concat([
    d[["STATE","LOW","WAGE_ST"]].rename(columns={"WAGE_ST":"WAGE"}).assign(POST=0),
    d[["STATE","LOW","WAGE_ST2"]].rename(columns={"WAGE_ST2":"WAGE"}).assign(POST=1)
], ignore_index=True)).fit()
print("\n===== 工资的三重差分（验证低薪店确实被处理得更狠）=====")
print(m_wage.summary().tables[1])

out = open("outputs/tables/extension.txt", "w", encoding="utf-8")
out.write("=== 扩展：低薪店 vs 高薪店 ===\n\n")
out.write("【NJ 内部 DiD】\n" + str(m_nj.summary().tables[1]) + "\n\n")
out.write("【三重差分 DDD】\n" + str(m_ddd.summary().tables[1]) + "\n\n")
out.write("【工资 DDD（验证处理强度）】\n" + str(m_wage.summary().tables[1]) + "\n")
out.close()
print("\n结果已写入 outputs/tables/extension.txt")