# Day 14 PM – Part D: AI-Augmented Task

## 1. Exact Prompt Used

> Give me 3 SQL interview questions at senior data engineer level involving window functions or CTEs. Include the expected answer and a common mistake candidates make for each question. Use standard ANSI SQL against a typical employees/departments/orders schema.

---

## 2. AI-Generated Questions, Answers, and Common Mistakes

### Question 1 – Running totals with partitions

**Question**

You have an `orders` table with columns `(order_id, customer_id, order_date, amount)`. Write a query that returns, for each customer and order, the cumulative sum of `amount` ordered by `order_date`. Only include orders from 2024.

**Expected Answer**

```sql
SELECT
    customer_id,
    order_id,
    order_date,
    amount,
    SUM(amount) OVER (
        PARTITION BY customer_id
        ORDER BY order_date,
                 order_id
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total
FROM orders
WHERE order_date >= DATE '2024-01-01'
  AND order_date < DATE '2025-01-01'
ORDER BY customer_id, order_date, order_id;
```

**Common Mistake**

Using `SUM(amount)` with `GROUP BY customer_id, order_date` instead of a window function, which collapses rows and loses per-order detail.

---

### Question 2 – Top-N per group with ties

**Question**

You have `employees(emp_id, emp_name, department_id, salary)` and `departments(dept_id, dept_name)`. Write a query to find the top 3 highest-paid employees per department, including ties (if multiple employees share the 3rd highest salary, include them all).

**Expected Answer**

```sql
WITH ranked AS (
    SELECT
        e.emp_id,
        e.emp_name,
        e.department_id,
        e.salary,
        DENSE_RANK() OVER (
            PARTITION BY e.department_id
            ORDER BY e.salary DESC
        ) AS salary_rank
    FROM employees e
)
SELECT
    r.emp_id,
    r.emp_name,
    r.department_id,
    r.salary
FROM ranked r
WHERE r.salary_rank <= 3
ORDER BY r.department_id, r.salary DESC, r.emp_name;
```

**Common Mistake**

Using `ROW_NUMBER()` instead of `DENSE_RANK()`, which incorrectly drops tied employees at the cutoff.

---

### Question 3 – CTE for complex filtering and aggregation

**Question**

Given `orders(order_id, customer_id, order_date, amount)` and `customers(customer_id, city)`, write a query to find cities where the last 3 months of revenue are at least 20% higher than the previous 3 months combined. Use CTEs and window functions.

**Expected Answer**

```sql
WITH monthly_revenue AS (
    SELECT
        c.city,
        DATE_TRUNC('month', o.order_date) AS month,
        SUM(o.amount) AS revenue
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    GROUP BY c.city, DATE_TRUNC('month', o.order_date)
), ranked_months AS (
    SELECT
        city,
        month,
        revenue,
        ROW_NUMBER() OVER (
            PARTITION BY city
            ORDER BY month DESC
        ) AS rn
    FROM monthly_revenue
), last_prev AS (
    SELECT
        city,
        SUM(CASE WHEN rn BETWEEN 1 AND 3 THEN revenue ELSE 0 END) AS last_3_rev,
        SUM(CASE WHEN rn BETWEEN 4 AND 6 THEN revenue ELSE 0 END) AS prev_3_rev
    FROM ranked_months
    WHERE rn <= 6
    GROUP BY city
)
SELECT
    city,
    last_3_rev,
    prev_3_rev
FROM last_prev
WHERE prev_3_rev > 0
  AND last_3_rev >= 1.2 * prev_3_rev
ORDER BY city;
```

**Common Mistake**

Forgetting to constrain the window to the last 6 months per city and instead using a running window over all history, which changes the business meaning of the comparison.

---

## 3. Testing Notes

I will adapt the AI-generated questions to the actual lab schema and run them on the database:

- For Question 1, use the real `orders` table and check that the running total matches manual checks for a few customers.
- For Question 2, use `employees` and `departments` data, and verify that tied salaries at rank 3 are included.
- For Question 3, aggregate by city and month on the real orders/customers tables and confirm that the last/previous three-month windows are correct for a few example cities.

I will also run `EXPLAIN` on each query to see whether indexes are used effectively and whether the use of window functions is reasonable given the table sizes.

---

## 4. Critical Evaluation (Approx. 200 Words)

The AI-generated questions are appropriate for a senior data engineer level because they combine window functions, partitioning logic, and multi-step CTEs that mirror real reporting and analytics scenarios. The first question tests understanding of cumulative sums per group and the importance of `ORDER BY` and frame clauses. The second question focuses on the subtle difference between `ROW_NUMBER()` and `DENSE_RANK()` when selecting top-N with ties, which often comes up in ranking and bonus calculations. The third question requires structuring a multi-step aggregation with CTEs, combining time series logic and percentage comparisons.

The common mistakes described are realistic but could be more specific. For example, in Question 1 the mistake could also mention forgetting the frame clause, which defaults to `RANGE` in some databases and can cause unexpected behavior when there are duplicate timestamps. In Question 3, another common mistake is not handling cities with fewer than six months of history correctly. The answers are syntactically correct and logically sound but assume a PostgreSQL-like environment due to `DATE_TRUNC`. For very large datasets, it would be worth discussing performance considerations such as partitioning by date, using appropriate indexes, and limiting the time range before applying window functions.
