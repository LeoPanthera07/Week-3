# Day 14 AM – Part C: Interview Ready

## Q1 – Logical execution order of a SQL SELECT

A SQL `SELECT` statement is written in one order but logically executed in a different order. The typical logical execution order is:

1. `FROM` (and `JOIN`)
2. `WHERE`
3. `GROUP BY`
4. `HAVING`
5. `SELECT`
6. `DISTINCT`
7. `ORDER BY`
8. `LIMIT` / `OFFSET`

This matters because aliases and expressions are only available in clauses that run **after** they are defined.

- Column aliases defined in `SELECT` cannot be used in `WHERE` or `GROUP BY`, because those clauses are evaluated earlier.
- Column aliases **can** be used in `ORDER BY`, because sorting happens after `SELECT`.
- Table aliases introduced in `FROM`/`JOIN` can be used everywhere later in the query.

Example:

```sql
SELECT
    e.emp_name,
    e.salary,
    e.salary * 0.10 AS bonus
FROM employees e
WHERE e.salary > 70000
ORDER BY bonus DESC;
```

Here, `bonus` cannot be referenced in `WHERE`, but it is valid in `ORDER BY`.

---

## Q2 – Employee salary vs department average and company average

Requirement: In a single query (no CTEs), show each employee’s name, salary, and their department average salary, **only for employees earning above the company-wide average salary**.

One practical solution is to combine a window function for the department average with a scalar subquery for the company-wide average:

```sql
SELECT
    emp_name,
    salary,
    AVG(salary) OVER (PARTITION BY department_id) AS dept_avg_salary
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);
```

Explanation:

- `AVG(salary) OVER (PARTITION BY department_id)` computes the department average for each row without collapsing rows.
- The scalar subquery `(SELECT AVG(salary) FROM employees)` computes the overall company average once.
- The `WHERE` clause filters to employees whose salary is above the company-wide average.

This returns one row per qualifying employee with their individual salary and their department’s average salary.

---

## Q3 – Debugging the AVG/WHERE query

Original buggy query:

```sql
SELECT department, AVG(salary) as avg_sal
FROM employees
WHERE AVG(salary) > 70000
GROUP BY department;
```

Bugs:

1. `AVG(salary)` is an aggregate function and cannot be used directly in the `WHERE` clause. Aggregates must be used in `SELECT`, `HAVING`, or `ORDER BY` (depending on SQL dialect), not in `WHERE`.
2. The filter `AVG(salary) > 70000` should apply **after** grouping by department. That is the purpose of the `HAVING` clause.

Corrected query:

```sql
SELECT
    department,
    AVG(salary) AS avg_sal
FROM employees
GROUP BY department
HAVING AVG(salary) > 70000;
```

Explanation:

- First, rows are grouped by `department`.
- Then `AVG(salary)` is computed per department.
- `HAVING` filters departments whose average salary is greater than 70000.
- The final result shows only departments meeting that condition, with their average salary.
