import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql://user:password@localhost:5432/company_db")

employees = pd.read_sql("SELECT * FROM employees", engine)
departments = pd.read_sql("SELECT * FROM departments", engine)
orders = pd.read_sql("SELECT * FROM orders", engine)

q1 = employees[["emp_id", "emp_name", "salary"]]

q2 = employees.loc[employees["salary"] > 80000, ["emp_name", "salary"]].sort_values("salary", ascending=False).head(3)

q3 = employees.loc[employees["hire_date"] >= "2021-01-01", ["emp_name", "hire_date"]].sort_values("hire_date")

q4 = pd.DataFrame({"total_employees": [len(employees)]})

q5 = employees.groupby("department_id", as_index=False)["salary"].mean().rename(columns={"salary": "avg_salary"})

q6 = employees.groupby("department_id", as_index=False).size().rename(columns={"size": "emp_count"}).loc[lambda df: df["emp_count"] >= 2]

q7 = employees.merge(departments, left_on="department_id", right_on="dept_id", how="inner")[["emp_id", "emp_name", "dept_name", "salary"]]

q8 = departments.merge(employees, left_on="dept_id", right_on="department_id", how="left")[["dept_name", "emp_name"]].sort_values(["dept_name", "emp_name"])

q9 = departments.merge(employees, left_on="dept_id", right_on="department_id", how="right")[["dept_name", "emp_name"]].sort_values(["dept_name", "emp_name"])

q10 = departments.merge(employees, left_on="dept_id", right_on="department_id", how="outer")[["dept_name", "emp_name"]].sort_values(["dept_name", "emp_name"])

q11 = employees.merge(orders, on="emp_id", how="inner")[["emp_name", "order_id", "amount"]].sort_values("amount", ascending=False)

tmp = departments.merge(employees, left_on="dept_id", right_on="department_id", how="inner").merge(orders, on="emp_id", how="inner")
q12 = tmp.groupby("dept_name", as_index=False)["amount"].sum().rename(columns={"amount": "total_revenue"}).sort_values("total_revenue", ascending=False)

q13 = departments.merge(employees, left_on="dept_id", right_on="department_id", how="left")
q13 = q13.loc[q13["emp_id"].isna(), ["dept_name", "emp_name"]]

avg_salary = employees["salary"].mean()
q14 = employees.loc[employees["salary"] > avg_salary, ["emp_name", "salary"]].sort_values("salary", ascending=False)

q15 = employees.assign(salary_rank=employees["salary"].rank(method="dense", ascending=False))[["emp_name", "salary_rank"]]