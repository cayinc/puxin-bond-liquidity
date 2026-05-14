import pandas as pd
import json
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "data.xlsx")

def clean_value(val):
    if pd.isna(val):
        return None
    if isinstance(val, pd.Timestamp):
        return val.strftime('%Y-%m-%d')
    if isinstance(val, float):
        if val == int(val):
            return int(val)
        return round(val, 4)
    return val

# ===================== Sheet1: TKN统计 =====================
df1 = pd.read_excel(file_path, sheet_name="TKN统计")
sheet1 = {
    "name": "TKN统计",
    "headers": [str(c) for c in df1.columns],
    "data": [[clean_value(row[c]) for c in df1.columns] for _, row in df1.iterrows()]
}

# ===================== Sheet2: 换手率&成交量 =====================
df2_raw = pd.read_excel(file_path, sheet_name="换手率&成交量", header=None)
sub_labels = ["整体", "(0,1)", "[1,3)", "[3,5)", "[5,7)", "[7,+)"]
sheet2_headers = ["日期",
    "成交量-整体","成交量-(0,1)","成交量-[1,3)","成交量-[3,5)","成交量-[5,7)","成交量-[7,+)",
    "换手率-整体","换手率-(0,1)","换手率-[1,3)","换手率-[3,5)","换手率-[5,7)","换手率-[7,+)",
    "换手率MA7-整体","换手率MA7-(0,1)","换手率MA7-[1,3)","换手率MA7-[3,5)","换手率MA7-[5,7)","换手率MA7-[7,+)"
]
sheet2_data = []
for i in range(4, len(df2_raw)):
    row = df2_raw.iloc[i]
    if pd.isna(row[0]):
        continue
    rec = [
        clean_value(row[0]),
        clean_value(row[3]), clean_value(row[4]), clean_value(row[5]),
        clean_value(row[6]), clean_value(row[7]), clean_value(row[8]),
        clean_value(row[11]), clean_value(row[12]), clean_value(row[13]),
        clean_value(row[14]), clean_value(row[15]), clean_value(row[16]),
        clean_value(row[19]), clean_value(row[20]), clean_value(row[21]),
        clean_value(row[22]), clean_value(row[23]), clean_value(row[24]),
    ]
    sheet2_data.append(rec)

sheet2 = {
    "name": "换手率&成交量",
    "headers": sheet2_headers,
    "data": sheet2_data,
    "groups": [
        {"label": "成交量（总和）", "cols": list(range(1, 7)), "sub": sub_labels},
        {"label": "换手率", "cols": list(range(7, 13)), "sub": sub_labels},
        {"label": "换手率MA7", "cols": list(range(13, 19)), "sub": sub_labels},
    ]
}

# ===================== Sheet3: 机构净买入普信 =====================
# 新版结构（260509）:
#
# 左表（按机构→期限分类）:
#   行1: 债券类型(普信) c0-c42
#   行2: 机构名 c0=机构, c1-36=明细机构, c37-42=合计机构
#   行3: 期限  c1-36=具体期限, c37-42=机构名（合计列的行3标注机构名）
#   数据: row4+ col0=日期, c1-36=明细, c37-42=各机构合计
#
#   明细列分布（6机构×6期限）:
#     c1-6  : 中小型银行 × [≦1Y,1-3Y,3-5Y,5-7Y,7-10Y,>10Y]
#     c7-12 : 保险公司   × [≦1Y,1-3Y,3-5Y,5-7Y,7-10Y,>10Y]
#     c13-18: 其他       × [≦1Y,1-3Y,3-5Y,5-7Y,7-10Y,>10Y]
#     c19-24: 基金公司及产品 × [≦1Y,1-3Y,3-5Y,5-7Y,7-10Y,>10Y]
#     c25-30: 理财子公司及理财类产品 × [≦1Y,1-3Y,3-5Y,5-7Y,7-10Y,>10Y]
#     c31-36: 证券公司   × [≦1Y,1-3Y,3-5Y,5-7Y,7-10Y,>10Y]
#   合计列（行3标注机构名作为标识）:
#     c37=农商行合计, c38=保险合计, c39=其他合计, c40=基金合计, c41=理财合计, c42=证券公司合计
#
# 右表（按期限→机构分类）:
#   行1: 债券类型(普信) c44-c80
#   行2: 期限 c44=期限(标题), c45-80=具体期限
#   行3: 机构 c44=机构(标题), c45-80=具体机构
#   数据: row4+ col44=空(分隔), c45-80=明细数据
#
#   明细列分布（6期限×6机构）:
#     c45-50 : ≦1Y  × [农商行,券商,保险,基金,理财,其他产品]
#     c51-56 : 1-3Y × [农商行,券商,保险,基金,理财,其他产品]
#     c57-62 : 3-5Y × [农商行,券商,保险,基金,理财,其他产品]
#     c63-68 : 5-7Y × [农商行,券商,保险,基金,理财,其他产品]
#     c69-74 : 7-10Y× [农商行,券商,保险,基金,理财,其他产品]
#     c75-80 : 10-15Y×[农商行,券商,保险,基金,理财,其他产品]

df3_raw = pd.read_excel(file_path, sheet_name="机构净买入普信", header=None)

# ---- 左表解析 ----
left_inst_map = {
    1: "中小型银行", 2: "中小型银行", 3: "中小型银行", 4: "中小型银行", 5: "中小型银行", 6: "中小型银行",
    7: "保险公司",   8: "保险公司",   9: "保险公司",   10: "保险公司",  11: "保险公司",  12: "保险公司",
    13: "其他",      14: "其他",      15: "其他",      16: "其他",      17: "其他",      18: "其他",
    19: "基金公司及产品", 20: "基金公司及产品", 21: "基金公司及产品", 22: "基金公司及产品", 23: "基金公司及产品", 24: "基金公司及产品",
    25: "理财子公司及理财类产品", 26: "理财子公司及理财类产品", 27: "理财子公司及理财类产品",
    28: "理财子公司及理财类产品", 29: "理财子公司及理财类产品", 30: "理财子公司及理财类产品",
    31: "证券公司",  32: "证券公司",  33: "证券公司",  34: "证券公司",  35: "证券公司",  36: "证券公司",
}
left_mat_map = {}
for c in range(1, 37):
    v = df3_raw.iloc[3, c]
    if pd.notna(v):
        left_mat_map[c] = str(v).strip()

left_maturity_order = ["≦1Y", "1-3Y", "3-5Y", "5-7Y", "7-10Y", ">10Y"]
left_institutions = list(dict.fromkeys([left_inst_map[c] for c in range(1, 37)]))

# 合计列：行3标注的是机构名（作为合计标识）
left_summary_cols = {
    37: "农商行-合计", 38: "保险-合计", 39: "其他-合计",
    40: "基金-合计",  41: "理财-合计", 42: "证券公司-合计"
}

# ---- 右表解析 ----
right_mat_order = ["≦1Y", "1-3Y", "3-5Y", "5-7Y", "7-10Y", "10-15Y"]
right_inst_order = ["农商行", "券商", "保险", "基金", "理财", "其他产品"]
# c45-80: 6期限 × 6机构, 每期限从各自起始列
right_mat_start = {
    "≦1Y":   45, "1-3Y":  51, "3-5Y":  57,
    "5-7Y":  63, "7-10Y": 69, "10-15Y":75
}

# ---- 构建 records ----
left_records = []
right_records = []

for row_idx in range(4, len(df3_raw)):
    row = df3_raw.iloc[row_idx]
    if pd.isna(row[0]):
        continue
    date = clean_value(row[0])

    # 左表明细
    for col in range(1, 37):
        inst = left_inst_map.get(col)
        mat  = left_mat_map.get(col)
        val  = clean_value(row[col])
        if inst and mat:
            left_records.append({
                "date": date, "institution": inst,
                "maturity": mat, "value": val, "is_summary": False
            })
    # 左表合计
    for col, label in left_summary_cols.items():
        val = clean_value(row[col])
        left_records.append({
            "date": date, "institution": label,
            "maturity": "合计", "value": val, "is_summary": True
        })

    # 右表明细
    for mat, start_col in right_mat_start.items():
        for i, inst in enumerate(right_inst_order):
            col = start_col + i
            val = clean_value(row[col])
            right_records.append({
                "date": date, "maturity": mat,
                "institution": inst, "value": val
            })

sheet3 = {
    "name": "机构净买入普信",
    # 左表信息
    "left_institutions": left_institutions,
    "left_maturities":   left_maturity_order,
    "left_summary_labels": list(left_summary_cols.values()),
    "left_records":       left_records,
    # 右表信息
    "right_maturities":   right_mat_order,
    "right_institutions": right_inst_order,
    "right_records":      right_records,
    # 兼容旧字段（图表仍使用左表合计）
    "institutions": left_institutions,
    "maturities":   left_maturity_order,
    "summary_labels": list(left_summary_cols.values()),
    "records": left_records,
}

# ===================== Sheet4: 普信&二永日度换手率 =====================
df4_raw = pd.read_excel(file_path, sheet_name="普信&二永日度换手率", header=None)
# 行0=空, 行1=标题(日期/普信/二永), 数据从行2开始
sheet4_dates = []
sheet4_puxin = []
sheet4_eryon = []
for i in range(2, len(df4_raw)):
    row = df4_raw.iloc[i]
    if pd.isna(row[0]):
        continue
    sheet4_dates.append(clean_value(row[0]))
    sheet4_puxin.append(round(float(row[1]) * 100, 4) if pd.notna(row[1]) else None)
    sheet4_eryon.append(round(float(row[2]) * 100, 4) if pd.notna(row[2]) else None)

sheet4 = {
    "name": "普信&二永日度换手率",
    "dates": sheet4_dates,
    "series": [
        {"name": "普信债", "data": sheet4_puxin, "color": "#1a73e8"},
        {"name": "二永债", "data": sheet4_eryon, "color": "#34a853"},
    ]
}

# ===================== Combine & Embed =====================
all_data = {
    "sheet1": sheet1,
    "sheet2": sheet2,
    "sheet3": sheet3,
    "sheet4": sheet4,
}

json_str = json.dumps(all_data, ensure_ascii=False, default=str)
print(f"Data JSON size: {len(json_str)/1024:.1f} KB")
print(f"Sheet3 left_records: {len(left_records)}")
print(f"Sheet3 right_records: {len(right_records)}")
print(f"Sheet4 dates count: {len(sheet4_dates)}")

with open("page_data.json", "w", encoding="utf-8") as f:
    json.dump(all_data, f, ensure_ascii=False, default=str)

print("✅ page_data.json 生成完成")
