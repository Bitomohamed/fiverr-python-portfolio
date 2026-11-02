"""
Project 3 — Employment History → Current State Analysis
Reads:  employment_history.csv
Writes: clean_employment_history.csv + current_employees.csv + summary
"""
import pandas as pd
import json

df = pd.read_csv("employment_history.csv")

# 1) Standardize dates
df["effective_from"] = pd.to_datetime(df["effective_from"], errors="coerce")
df["effective_to"]   = pd.to_datetime(df["effective_to"], errors="coerce")

# 2) Standardize change_reason
df["change_reason"] = df["change_reason"].astype(str).str.strip().str.title()

# 3) Flag current vs historical
today = pd.Timestamp.today().normalize()
df["is_current"] = df["effective_to"].isna() | (df["effective_to"] > today)

# 4) Save full history (cleaned)
df.to_csv("clean_employment_history.csv", index=False)

# 5) Build current snapshot (latest record per employee)
current = (
    df.sort_values("effective_from")
    .groupby("emp_id", as_index=False)
    .last()
)

# 6) Tenure — from HIRE date (earliest record)
first_hire = (
    df.sort_values("effective_from")
    .groupby("emp_id", as_index=False)
    .first()[["emp_id", "effective_from"]]
    .rename(columns={"effective_from": "hire_date"})
)

current = current.merge(first_hire, on="emp_id", how="left")
current["tenure_days"]  = (today - current["hire_date"]).dt.days
current["tenure_years"] = (current["tenure_days"] / 365.25).round(2)

# 7) Salary bands
current["salary_band"] = pd.cut(
    current["basic_salary"],
    bins=[0, 30000, 50000, 75000, 100000, 150000, float("inf")],
    labels=["<30K", "30K-50K", "50K-75K", "75K-100K", "100K-150K", "150K+"],
)

# 8) Format dates
current["effective_from"] = current["effective_from"].dt.strftime("%Y-%m-%d")
current["effective_to"]   = current["effective_to"].dt.strftime("%Y-%m-%d")
current["hire_date"]      = current["hire_date"].dt.strftime("%Y-%m-%d")
current.to_csv("current_employees.csv", index=False)

# 9) Summary
summary = {
    "total_history_records": len(df),
    "unique_employees": int(df["emp_id"].nunique()),
    "current_employees": len(current),
    "change_reasons": df["change_reason"].value_counts().to_dict(),
    "avg_tenure_from_hire_years":   round(current["tenure_years"].mean(), 2),
    "median_tenure_from_hire_years": round(current["tenure_years"].median(), 2),
    "avg_current_salary": int(current["basic_salary"].mean()),
    "median_salary": int(current["basic_salary"].median()),
    "salary_bands": current["salary_band"].value_counts().sort_index().to_dict(),
    "departments_top5": current["dept_id"].value_counts().head(5).to_dict(),
}
print(json.dumps(summary, indent=2, ensure_ascii=False, default=str))