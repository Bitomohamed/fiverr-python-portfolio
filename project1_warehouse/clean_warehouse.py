"""
Project 1 — Warehouse Inventory Cleanup
Reads:  warehouse_messy_data.csv
Writes: clean_warehouse.csv + summary
"""
import pandas as pd
import json

df = pd.read_csv("warehouse_messy_data.csv")
original_rows = len(df)

# 1) Product Name: strip whitespace + Title Case
df["Product Name"] = df["Product Name"].astype(str).str.strip().str.title()

# 2) Category: ALL CAPS → Title Case
df["Category"] = df["Category"].astype(str).str.strip().str.title()

# 3) Quantity: "two hundred" → 200
def parse_quantity(q):
    if pd.isna(q): return None
    s = str(q).strip().lower()
    text_map = {
        "two hundred": 200, "one hundred": 100,
        "three hundred": 300, "fifty": 50,
    }
    if s in text_map: return text_map[s]
    try: return int(float(s))
    except (ValueError, TypeError): return None

df["Quantity"] = df["Quantity"].apply(parse_quantity)

# 4) Price: "NaN" string → pd.NA
df["Price"] = pd.to_numeric(
    df["Price"].replace("NaN", pd.NA), errors="coerce"
)

# 5) Last Restocked: 3 formats + "NaN"
def parse_date(d):
    if pd.isna(d): return None
    s = str(d).strip()
    if s in ("NaN", "nan", ""): return None
    for fmt in ["%d/%m/%Y", "%Y-%m-%d", "%m/%d/%Y"]:
        try: return pd.to_datetime(s, format=fmt)
        except (ValueError, TypeError): continue
    return pd.to_datetime(s, errors="coerce")

df["Last Restocked"] = df["Last Restocked"].apply(parse_date)

# 6) Status: standardize
df["Status"] = df["Status"].astype(str).str.strip().str.title()

# 7) Handle duplicate Product IDs: keep the one with latest restock
dupe_count = int(df.duplicated(subset=["Product ID"]).sum())
df = df.sort_values("Last Restocked", na_position="first")
df = df.drop_duplicates(subset=["Product ID"], keep="last")

# 8) Format dates as ISO
df["Last Restocked"] = df["Last Restocked"].dt.strftime("%Y-%m-%d")

df = df.sort_values("Product ID").reset_index(drop=True)
df.to_csv("clean_warehouse.csv", index=False)

summary = {
    "original_rows": original_rows,
    "final_rows": len(df),
    "duplicates_by_product_id_removed": dupe_count,
    "quantity_text_converted": "'two hundred' → 200",
    "price_nan_strings_fixed": int(df["Price"].isna().sum()),
    "date_formats_unified": "3 formats → ISO 8601",
    "missing_restock_dates_after_clean": int(df["Last Restocked"].isna().sum()),
    "products_by_status": df["Status"].value_counts().to_dict(),
}
print(json.dumps(summary, indent=2, ensure_ascii=False))