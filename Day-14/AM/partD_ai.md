# Day 14 AM – Part D: AI-Augmented Task

## 1. Exact Prompt Used

> Generate 5 medium-difficulty SQL interview questions for a data engineer role, with answers. Include one about JOINs, one about NULL handling, and one about performance. Use standard ANSI SQL against a typical employees/departments/orders schema.

---

## 2. AI-Generated Questions and Answers

### Q1 – JOINs

**Question**

Write a SQL query to list each employee’s name, their department name, and the total amount of orders they handled. Include employees who have not handled any orders, showing the total as 0.

**Answer**

```sql
SELECT
    e.emp_name,
    d.dept_name,
    COALESCE(SUM(o.amount), 0) AS total_orders
FROM employees e
JOIN departments d ON e.department_id = d.dept_id
LEFT JOIN orders o ON e.emp_id = o.emp_id
GROUP BY e.emp_name, d.dept_name
ORDER BY total_orders DESC;
```

---

### Q2 – NULL Handling

**Question**

You have a `customers` table with columns `customer_id`, `name`, and `email`. Some customers do not have an email address. Write a query that returns two counts: number of customers with an email and number of customers without an email.

**Answer**

```sql
SELECT
    SUM(CASE WHEN email IS NOT NULL AND email <> '' THEN 1 ELSE 0 END) AS with_email,
    SUM(CASE WHEN email IS NULL OR email = '' THEN 1 ELSE 0 END) AS without_email
FROM customers;
```

---

### Q3 – Aggregations and HAVING

**Question**

Given an `orders` table with columns `order_id`, `customer_id`, and `amount`, write a query to find customers whose total order amount is greater than 10,000. Return `customer_id` and `total_amount`.

**Answer**

```sql
SELECT
    customer_id,
    SUM(amount) AS total_amount
FROM orders
GROUP BY customer_id
HAVING SUM(amount) > 10000
ORDER BY total_amount DESC;
```

---

### Q4 – Performance and Indexing

**Question**

You frequently run the query below, and it has become slow as the `orders` table grew:

```sql
SELECT *
FROM orders
WHERE order_date >= CURRENT_DATE - INTERVAL '30 days'
ORDER BY order_date DESC;
```

What index would you create to improve performance, and why?

**Answer**

You can create an index on `order_date`:

```sql
CREATE INDEX idx_orders_order_date
    ON orders (order_date DESC);
```

This helps the database quickly locate recent rows by `order_date` and avoid a full table scan for the last 30 days, and the ordering matches the query’s `ORDER BY`.

---

### Q5 – Window Functions

**Question**

Given an `employees` table with `emp_id`, `emp_name`, `department_id`, and `salary`, write a query that returns each employee’s name, salary, and their department rank by salary (1 = highest salary in that department).

**Answer**

```sql
SELECT
    emp_name,
    salary,
    RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) AS dept_salary_rank
FROM employees
ORDER BY department_id, dept_salary_rank;
```

---

## 3. Testing Notes

I will run each of the five AI-generated queries (or CREATE INDEX) against the course database schema once the relevant tables exist:

- For Q1 and Q5, I will use the existing `employees`, `departments`, and `orders` tables.
- For Q2, I will either create a simple `customers` table or adapt the query to the available customer-like table.
- For Q3, I will run the aggregation against the real `orders` data.
- For Q4, I will run `EXPLAIN` before and after creating the suggested index to confirm reduced cost and better index usage.

I will verify that each query runs without syntax errors and that the results are logically correct for the data.

---

## 4. Critical Evaluation (Approx. 200 Words)

The AI-generated questions are generally in the medium-difficulty range. They cover JOINs, NULL handling, aggregations with HAVING, indexing for performance, and window functions, which are all relevant for a data engineer role. The JOIN question correctly uses an inner join plus a left join and `COALESCE` to include employees without orders, which is realistic. The NULL-handling question uses `CASE` expressions that distinguish between NULL and empty strings, which is a common pitfall.

However, the questions could be made slightly more challenging by adding more complex join conditions, multi-column grouping, or edge cases like multiple indexes and composite keys. The performance question is somewhat high-level; it suggests a reasonable index but does not discuss trade-offs, index selectivity, or covering indexes. The answers are syntactically correct and would run on a standard schema with minimal adaptation, but they do not show `EXPLAIN` plans or measurement of actual performance.

Overall, the AI output is a good starting point but would benefit from small tweaks to align exactly with the course schema and to push candidates a bit further on query tuning and reasoning about execution plans rather than just syntax.
