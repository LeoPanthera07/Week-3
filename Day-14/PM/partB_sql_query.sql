WITH RECURSIVE nums AS (
    SELECT 1 AS n
    UNION ALL
    SELECT n + 1 FROM nums WHERE n < 100
)
SELECT n FROM nums ORDER BY n;

WITH RECURSIVE nums AS (
    SELECT 1 AS n
    UNION ALL
    SELECT n + 1 FROM nums WHERE n < 100
),
bounds AS (
    SELECT MIN(sale_date)::date AS start_date,
           MAX(sale_date)::date AS end_date
    FROM sales
),
date_series AS (
    SELECT (SELECT start_date FROM bounds) + (n - 1) * INTERVAL '1 day' AS dt
    FROM nums
),
filtered_series AS (
    SELECT dt::date AS dt
    FROM date_series, bounds
    WHERE dt::date BETWEEN bounds.start_date AND bounds.end_date
),
daily_revenue AS (
    SELECT sale_date::date AS dt, SUM(amount) AS revenue
    FROM sales
    GROUP BY sale_date::date
)
SELECT
    f.dt AS date,
    COALESCE(d.revenue, 0) AS revenue
FROM filtered_series f
LEFT JOIN daily_revenue d ON d.dt = f.dt
ORDER BY f.dt;
