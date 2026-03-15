# Day 14 PM – Part C: Interview Ready

## Q1 – RANK() vs DENSE_RANK()

`RANK()` and `DENSE_RANK()` are both window functions used to assign ranks based on an `ORDER BY` clause, but they handle ties differently.

- `RANK()` leaves gaps in the ranking when there are ties.
- `DENSE_RANK()` does not leave gaps; the next distinct value gets the next immediate rank.

Example:

```sql
SELECT
    emp_name,
    salary,
    RANK() OVER (ORDER BY salary DESC) AS rnk,
    DENSE_RANK() OVER (ORDER BY salary DESC) AS dense_rnk
FROM employees
ORDER BY salary DESC;
```

If salaries are: 100, 90, 90, 80, then:

- `RANK()` gives: 1, 2, 2, 4
- `DENSE_RANK()` gives: 1, 2, 2, 3

The difference matters in business contexts such as:

- Bonus bands: if three people tie for first, you might use `DENSE_RANK()` so the next band is rank 2, not 4.
- Reporting top‑N lists: when counting “top 3 performers”, `DENSE_RANK()` ensures that only 3 distinct ranks exist, even if there are ties.
- Audit and compliance: sometimes gaps (from `RANK()`) are desirable to show that positions were skipped due to ties.

Choosing between them depends on whether you want to count **distinct values** (use `DENSE_RANK()`) or **positions** including gaps (use `RANK()`).

---

## Q2 – Users with purchases in 3+ consecutive months

Given a table:

```sql
transactions(user_id, transaction_date, amount)
```

We can:

1. Aggregate to one row per user and month.
2. Use `LAG()` to detect consecutive months.
3. Use a running group identifier to find streaks.

```sql
WITH monthly AS (
    SELECT
        user_id,
        DATE_TRUNC('month', transaction_date) AS month
    FROM transactions
    GROUP BY user_id, DATE_TRUNC('month', transaction_date)
), with_lag AS (
    SELECT
        user_id,
        month,
        LAG(month) OVER (
            PARTITION BY user_id
            ORDER BY month
        ) AS prev_month
    FROM monthly
), groups AS (
    SELECT
        user_id,
        month,
        SUM(
            CASE
                WHEN prev_month IS NULL
                     OR month <> prev_month + INTERVAL '1 month'
                THEN 1
                ELSE 0
            END
        ) OVER (
            PARTITION BY user_id
            ORDER BY month
        ) AS grp
    FROM with_lag
), streaks AS (
    SELECT
        user_id,
        grp,
        COUNT(*) AS months_in_streak
    FROM groups
    GROUP BY user_id, grp
)
SELECT DISTINCT user_id
FROM streaks
WHERE months_in_streak >= 3
ORDER BY user_id;
```

This returns all `user_id` values that have purchases in 3 or more consecutive calendar months.

---

## Q3 – Optimising the correlated subquery with a window function

Original query:

```sql
SELECT name, salary
FROM employees e1
WHERE salary > (
    SELECT AVG(salary)
    FROM employees e2
    WHERE e2.department = e1.department
);
```

This is a correlated subquery: for each row in `employees e1`, the database runs a subquery that recomputes the average salary for that employee’s department. That can be `O(n²)` on large tables.

A more efficient version uses a window function to compute the department average once per row, then filters on it:

```sql
SELECT
    name,
    salary
FROM (
    SELECT
        name,
        salary,
        AVG(salary) OVER (
            PARTITION BY department
        ) AS dept_avg_salary
    FROM employees
) t
WHERE salary > dept_avg_salary;
```

Here:

- `AVG(salary) OVER (PARTITION BY department)` computes the average salary per department in a single pass over the table.
- The outer query simply filters rows where `salary` is greater than the precomputed `dept_avg_salary`.

This reduces repeated work compared to the correlated subquery and is typically easier for the optimizer to execute efficiently, especially on large `employees` tables.
