import pandas as pd
import random

random.seed(42)

names = ['grace','david','hannah','eve','jack','charlie','frank','bob','alice','ivy']
depts = ['HR','Finance','Sales','IT','Marketing']
positions = ['Manager','Director','Clerk','Analyst','Assistant']
genders = ['Male','Female','Other']
salaries = ['50000','65000','55000','70000','SIXTY THOUSAND',' NAN ','nan']
ages = ['25','thirty','35','40','50','nan']
dates = ['April 5, 2018','2020/02/20','01/15/2020','2019.12.01','03-25-2019']
phones = ['123-456-7890','098-765-4321','555-555-5555','','nan']

def make_email(name):
    domains = ['gmail.com','yahoo.com','outlook.com','company.org','business.net']
    return f"{name}{random.randint(1,999)}@{random.choice(domains)}"

rows = []
for i in range(1000):
    name = random.choice(names)
    r = random.random()

    if r < 0.70:
        email = make_email(name)                      # صالح
    elif r < 0.85:
        email = 'email@example.com'                   # placeholder
    elif r < 0.95:
        email = ''                                    # فارغ
    else:
        email = 'nan'                                 # نص nan

    rows.append([
        ' ' + name + ' ',
        random.choice(ages),
        random.choice(salaries),
        random.choice(genders),
        random.choice(depts),
        random.choice(positions),
        random.choice(dates),
        random.choice(['A','B','C','D','F']),
        email,
        random.choice(phones),
    ])

# أضف 100 صفوف مكررة (نفس البريد) لإظهار الحذف
existing = [r for r in rows if '@' in r[8] and r[8] not in ('email@example.com','nan','')]
for _ in range(100):
    dup = random.choice(existing).copy()
    dup[1] = random.choice(ages)
    dup[2] = random.choice(salaries)
    rows.append(dup)

random.shuffle(rows)

df = pd.DataFrame(rows, columns=['Name','Age','Salary','Gender','Department',
                                  'Position','Joining Date','Performance Score',
                                  'Email','Phone Number'])
df.to_csv('messy_HR_data.csv', index=False, encoding='utf-8-sig')
print(f"✅ Created messy_HR_data.csv with {len(df)} rows")
print(f"   Valid emails: {sum('@' in str(e) and e not in ('email@example.com','nan','') for e in df['Email'])}")
print(f"   Placeholders: {(df['Email'] == 'email@example.com').sum()}")
print(f"   Empty/nan:    {(df['Email'].isin(['', 'nan'])).sum()}")