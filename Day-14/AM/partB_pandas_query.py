import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql://user:password@localhost:5432/company_db")

employees = pd.read_sql("SELECT * FROM employees", engine)
departments = pd.read_sql("SELECT * FROM departments", engine)
projects = pd.read_sql("SELECT * FROM projects", engine)

j1 = (
    employees
    .merge(projects, left_on="emp_id", right_on="lead_emp_id", how="inner")
    .merge(departments, left_on="department_id", right_on="dept_id", how="inner")
)

q1 = (
    j1[["emp_name", "dept_name", "budget_y", "project_name", "budget_x"]]
    .rename(columns={"budget_y": "dept_budget", "budget_x": "project_budget"})
    .sort_values(["dept_name", "emp_name", "project_name"])
)

j2 = (
    departments
    .merge(employees, left_on="dept_id", right_on="department_id", how="inner")
    .merge(projects, left_on="emp_id", right_on="lead_emp_id", how="inner")
)

q2 = (
    j2.groupby(["dept_name", "budget_x"], as_index=False)["budget_y"]
    .sum()
    .rename(columns={"budget_x": "dept_budget", "budget_y": "total_project_budget"})
    .loc[lambda df: df["total_project_budget"] > df["dept_budget"]]
)