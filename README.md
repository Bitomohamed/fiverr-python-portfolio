@"
# ðŸ Python Data Cleaning & Analysis Portfolio

Three real-world portfolio projects built with Python and pandas, demonstrating
data cleaning, transformation, and analytical reporting.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![pandas](https://img.shields.io/badge/pandas-2.0+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## ðŸ“Œ Projects

| # | Project | Data Type | Key Problems Solved |
|---|---------|-----------|---------------------|
| 1 | **Warehouse Inventory Cleanup** | Product data | Text quantities, 3 date formats, 385 duplicate Product IDs |
| 2 | **HR Employee Data Cleanup** | Employee records | Text salaries, 4 date formats, 299 missing emails, 106 duplicates |
| 3 | **Employment History Analysis** | HR history table | History to current-state, tenure analysis, salary bands |

---

## ðŸ› ï¸ Tech Stack

- Python 3.10+
- pandas
- regex
- datetime

---

## ðŸš€ Quick Start

```bash
git clone https://github.com/Bitomohamed/fiverr-python-portfolio.git
cd fiverr-python-portfolio
pip install -r requirements.txt

cd project1_warehouse && python clean_warehouse.py
cd ../project2_hr_employee && python clean_hr.py
cd ../project3_employment_history && python analyze_history.py
