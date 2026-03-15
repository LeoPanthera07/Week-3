CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    city VARCHAR(50) NOT NULL
);

CREATE TABLE sales (
    sale_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id),
    city VARCHAR(50) NOT NULL,
    sale_date DATE NOT NULL,
    category VARCHAR(50) NOT NULL,
    amount NUMERIC(12, 2) NOT NULL
);

INSERT INTO customers (customer_name, city) VALUES
    ('Amit', 'Mumbai'),
    ('Priya', 'Mumbai'),
    ('Rohan', 'Delhi'),
    ('Neha', 'Delhi'),
    ('Kunal', 'Bengaluru'),
    ('Meera', 'Bengaluru');

INSERT INTO sales (customer_id, city, sale_date, category, amount) VALUES
    (1, 'Mumbai', '2024-01-05', 'Electronics', 12000),
    (1, 'Mumbai', '2024-01-15', 'Electronics', 8000),
    (2, 'Mumbai', '2024-01-20', 'Clothing', 3000),
    (2, 'Mumbai', '2024-02-10', 'Electronics', 15000),
    (3, 'Delhi', '2024-01-12', 'Home', 5000),
    (3, 'Delhi', '2024-03-01', 'Electronics', 9000),
    (4, 'Delhi', '2024-02-05', 'Clothing', 4000),
    (5, 'Bengaluru', '2024-01-25', 'Electronics', 7000),
    (5, 'Bengaluru', '2024-02-15', 'Home', 6000),
    (6, 'Bengaluru', '2024-03-05', 'Clothing', 3500);

SELECT
    category,
    sale_date,
    SUM(amount) AS daily_revenue,
    SUM(SUM(amount)) OVER (
        PARTITION BY category
        ORDER BY sale_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS cumulative_revenue
FROM sales
GROUP BY category, sale_date
ORDER BY category, sale_date;

WITH revenue_per_customer AS (
    SELECT
        city,
        customer_id,
        SUM(amount) AS total_revenue
    FROM sales
    GROUP BY city, customer_id
), ranked AS (
    SELECT
        r.city,
        r.customer_id,
        r.total_revenue,
        ROW_NUMBER() OVER (
            PARTITION BY r.city
            ORDER BY r.total_revenue DESC
        ) AS rn
    FROM revenue_per_customer r
)
SELECT
    c.city,
    c.customer_name,
    r.total_revenue
FROM ranked r
JOIN customers c ON r.customer_id = c.customer_id
WHERE r.rn <= 3
ORDER BY c.city, r.total_revenue DESC;

WITH monthly_revenue AS (
    SELECT
        DATE_TRUNC('month', sale_date) AS month,
        SUM(amount) AS revenue
    FROM sales
    GROUP BY DATE_TRUNC('month', sale_date)
), with_lag AS (
    SELECT
        month,
        revenue,
        LAG(revenue) OVER (ORDER BY month) AS prev_revenue
    FROM monthly_revenue
)
SELECT
    month,
    revenue,
    prev_revenue,
    CASE
        WHEN prev_revenue IS NULL THEN NULL
        WHEN prev_revenue = 0 THEN NULL
        ELSE (revenue - prev_revenue) / prev_revenue::NUMERIC * 100
    END AS mom_change_pct,
    CASE
        WHEN prev_revenue IS NOT NULL
             AND prev_revenue <> 0
             AND (revenue - prev_revenue) / prev_revenue::NUMERIC * 100 < -5
        THEN TRUE
        ELSE FALSE
    END AS flagged
FROM with_lag
ORDER BY month;

WITH company_avg AS (
    SELECT AVG(salary) AS avg_salary FROM employees
), dept_flags AS (
    SELECT
        e.department_id,
        MIN(CASE WHEN e.salary > c.avg_salary THEN 1 ELSE 0 END) AS all_above
    FROM employees e
    CROSS JOIN company_avg c
    GROUP BY e.department_id
)
SELECT
    d.dept_name
FROM dept_flags df
JOIN departments d ON d.dept_id = df.department_id
WHERE df.all_above = 1;

SELECT
    e1.department_id,
    e1.emp_name,
    e1.salary
FROM employees e1
WHERE 1 = (
    SELECT COUNT(DISTINCT e2.salary)
    FROM employees e2
    WHERE e2.department_id = e1.department_id
      AND e2.salary > e1.salary
);
