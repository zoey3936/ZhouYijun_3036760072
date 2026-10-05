# 04_replication_rest.py
# 第四步：补全 Table 2、Table 3 构成、Table 4 稳健性
# 所有结果写入 outputs/tables.txt，直接可以贴进报告

import pandas as pd
import statsmodels.formula.api as smf
import os

os.makedirs("outputs/tables", exist_ok=True)

out = open("outputs/tables/tables.txt", "w", encoding="utf-8")

df = pd.read_csv("data/raw/public.csv")
df["FTE"] = df["EMPFT"] + df["NMGRS"] + 0.5 * df["EMPPT"]
d = df[df["STATUS2"] == 1].copy()
d["FTE2"] = d["EMPFT2"] + d["NMGRS2"] + 0.5 * d["EMPPT2"]

def w(title, s):
    out.write(f"\n{'='*60}\n{title}\n{'='*60}\n{s}\n")

# ---------- Table 2 完整版：各变量 NJ vs PA × 前/后 ----------
w("Table 2. 各变量均值（政策前 FTE/WAGE_ST/价格，政策后加 2 后缀）",
  d.groupby("STATE")[["FTE","FTE2","WAGE_ST","WAGE_ST2","PSODA","PSODA2",
                      "PFRY","PFRY2","PENTREE","PENTREE2","HRSOPEN","HRSOPEN2"]].mean().round(3).to_string())

# ---------- Table 3 构成部分：门店特征 ----------
w("Table 3a. 样本构成：品牌分布",
  pd.crosstab(d["CHAIN"], d["STATE"], margins=True).to_string())
w("Table 3b. 样本构成：直营店占比",
  d.groupby("STATE")["CO_OWNED"].mean().round(3).to_string())

# ---------- Table 4 稳健性 ----------
# 长格式数据
db = d[["STATE","CHAIN","CO_OWNED","FTE"]].copy();  db["POST"]=0; db=db.rename(columns={"FTE":"EMP"})
da = d[["STATE","CHAIN","CO_OWNED","FTE2"]].copy(); da["POST"]=1; da=da.rename(columns={"FTE2":"EMP"})
long = pd.concat([db, da], ignore_index=True)

w("Table 4-1. 基准 DiD",
  str(smf.ols("EMP ~ STATE + POST + STATE:POST", data=long).fit().params.round(3)))
w("Table 4-2. 控制品牌（品牌固定效应）",
  str(smf.ols("EMP ~ STATE + POST + STATE:POST + C(CHAIN)", data=long).fit().params.round(3)))
w("Table 4-3. 只用 Burger King（CHAIN==1）",
  str(smf.ols("EMP ~ STATE + POST + STATE:POST", data=long[long.CHAIN==1]).fit().params.round(3)))
w("Table 4-4. 只用直营店",
  str(smf.ols("EMP ~ STATE + POST + STATE:POST", data=long[long.CO_OWNED==1]).fit().params.round(3)))
w("Table 4-5. 只用加盟店",
  str(smf.ols("EMP ~ STATE + POST + STATE:POST", data=long[long.CO_OWNED==0]).fit().params.round(3)))

out.close()
print("全部表格已写入 outputs/tables/tables.txt")