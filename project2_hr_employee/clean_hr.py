"""
Project 2 — HR Employee Data Cleanup
Reads:  messy_HR_data.csv
Writes: clean_hr.csv + summary
"""
import pandas as pd
import re
import json

df = pd.read_csv("messy_HR_data.csv")
original_rows = len(df)

# 1) Name
df["Name"] = df["Name"].astype(str).str.strip().str.title()

# 2) Age
def parse_age(a):
    if pd.isna(a): return None
    s = str(a).strip().lower()
    text_map = {"thirty": 30, "twenty": 20, "forty": 40, "fifty": 50}
    if s in text_map: return text_map[s]
    if s in ("nan", ""): return None
    try: return int(float(s))
    except (ValueError, TypeError): return None

df["Age"] = df["Age"].apply(parse_age)

# 3) Salary
def parse_salary(s):
    if pd.isna(s): return None
    txt = str(s).strip().upper()
    if txt in ("NAN", ""): return None
    if txt == "SIXTY THOUSAND": return 60000
    if txt == "FIFTY THOUSAND": return 50000
    try: return float(str(s).strip())
    except (ValueError, TypeError): return None

df["Salary"] = df["Salary"].apply(parse_salary)

# 4) Gender
df["Gender"] = df["Gender"].astype(str).str.strip().str.title()

# 5) Joining Date
def parse_date(d):
    if pd.isna(d): return None
    s = str(d).strip()
    for fmt in ["%B %d, %Y", "%Y/%m/%d", "%m/%d/%Y", "%Y.%m.%d"]:
        try: return pd.to_datetime(s, format=fmt)
        except (ValueError, TypeError): continue
    return pd.to_datetime(s, errors="coerce")

df["Joining Date"] = df["Joining Date"].apply(parse_date)

# 6) Email
PLACEHOLDERS = {"email@example.com", "name@company.org", "user@domain.com"}
EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

def clean_email(e):
    if pd.isna(e): return None
    s = str(e).strip().lower()
    if s in ("", "nan"): return None
    if s in PLACEHOLDERS: return None
    return s if EMAIL_REGEX.match(s) else None

df["Email"] = df["Email"].apply(clean_email)

# 7) Phone
def clean_phone(p):
    if pd.isna(p): return None
    s = str(p).strip().lower()
    if s in ("", "nan"): return None
    digits = re.sub(r"\D", "", s)
    if len(digits) == 10: return f"+1{digits}"
    if len(digits) == 11 and digits.startswith("1"): return f"+{digits}"
    return None

df["Phone Number"] = df["Phone Number"].apply(clean_phone)

# 8) Performance Score
VALID = {"A", "B", "C", "D", "F"}
df["Performance Score"] = df["Performance Score"].apply(
    lambda x: str(x).strip().upper()
    if pd.notna(x) and str(x).strip().upper() in VALID else None
)

# 9) Drop rows without email + deduplicate by email
before = len(df)
df = df.dropna(subset=["Email"])
dropped_no_email = before - len(df)

dupes = int(df.duplicated(subset=["Email"]).sum())
df = df.sort_values("Joining Date").drop_duplicates(subset=["Email"], keep="last")

# 10) Format dates
df["Joining Date"] = df["Joining Date"].dt.strftime("%Y-%m-%d")

df = df.reset_index(drop=True)
df.to_csv("clean_hr.csv", index=False)

summary = {
    "original_rows": original_rows,
    "final_rows": len(df),
    "dropped_no_email": dropped_no_email,
    "duplicates_by_email_removed": dupes,
    "age_fixed": "'thirty' / 'nan' → int / None",
    "salary_fixed": "'SIXTY THOUSAND' → 60000",
    "date_formats_unified": "4 formats → ISO 8601",
    "valid_emails": int(df["Email"].notna().sum()),
    "valid_phones": int(df["Phone Number"].notna().sum()),
    "placeholders_removed": "email@example.com, name@company.org, user@domain.com",
}
print(json.dumps(summary, indent=2, ensure_ascii=False))