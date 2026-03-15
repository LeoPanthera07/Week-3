CREATE TABLE departments (
    dept_id SERIAL PRIMARY KEY,
    dept_name VARCHAR(50) NOT NULL,
    budget NUMERIC(12, 2) NOT NULL
);

CREATE TABLE employees (
    emp_id SERIAL PRIMARY KEY,
    emp_name VARCHAR(50) NOT NULL,
    department_id INT REFERENCES departments(dept_id),
    salary NUMERIC(12, 2) NOT NULL,
    hire_date DATE NOT NULL
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    emp_id INT REFERENCES employees(emp_id),
    order_date DATE NOT NULL,
    amount NUMERIC(12, 2) NOT NULL
);

INSERT INTO departments (dept_name, budget) VALUES
    ('Engineering', 500000),
    ('Sales', 300000),
    ('HR', 150000),
    ('Marketing', 200000);

INSERT INTO employees (emp_name, department_id, salary, hire_date) VALUES
    ('Amit', 1, 90000, '2021-01-15'),
    ('Priya', 1, 120000, '2019-06-01'),
    ('Rohan', 2, 70000, '2020-03-10'),
    ('Neha', 2, 65000, '2022-02-20'),
    ('Kunal', 3, 55000, '2023-01-05'),
    ('Meera', 4, 80000, '2018-11-30');

INSERT INTO orders (emp_id, order_date, amount) VALUES
    (2, '2024-01-05', 50000),
    (2, '2024-02-10', 75000),
    (3, '2024-01-12', 20000),
    (4, '2024-03-01', 15000),
    (6, '2024-01-20', 30000);

SELECT emp_id, emp_name, salary FROM employees;

SELECT emp_name, salary FROM employees
WHERE salary > 80000
ORDER BY salary DESC
LIMIT 3;

SELECT emp_name, hire_date FROM employees
WHERE hire_date >= '2021-01-01'
ORDER BY hire_date;

SELECT COUNT(*) AS total_employees FROM employees;

SELECT department_id, AVG(salary) AS avg_salary
FROM employees
GROUP BY department_id;

SELECT department_id, COUNT(*) AS emp_count
FROM employees
GROUP BY department_id
HAVING COUNT(*) >= 2;

SELECT e.emp_id, e.emp_name, d.dept_name, e.salary
FROM employees e
JOIN departments d ON e.department_id = d.dept_id;

SELECT d.dept_name, e.emp_name
FROM departments d
LEFT JOIN employees e ON d.dept_id = e.department_id
ORDER BY d.dept_name, e.emp_name;

SELECT d.dept_name, e.emp_name
FROM departments d
RIGHT JOIN employees e ON d.dept_id = e.department_id
ORDER BY d.dept_name, e.emp_name;

SELECT d.dept_name, e.emp_name
FROM departments d
FULL OUTER JOIN employees e ON d.dept_id = e.department_id
ORDER BY d.dept_name, e.emp_name;

SELECT e.emp_name, o.order_id, o.amount
FROM employees e
JOIN orders o ON e.emp_id = o.emp_id
ORDER BY o.amount DESC;

SELECT d.dept_name, SUM(o.amount) AS total_revenue
FROM departments d
JOIN employees e ON d.dept_id = e.department_id
JOIN orders o ON e.emp_id = o.emp_id
GROUP BY d.dept_name
ORDER BY total_revenue DESC;

SELECT d.dept_name, e.emp_name
FROM departments d
LEFT JOIN employees e ON d.dept_id = e.department_id
WHERE e.emp_id IS NULL;

SELECT emp_name, salary
FROM employees
WHERE salary > (
    SELECT AVG(salary) FROM employees
)
ORDER BY salary DESC;

SELECT emp_name, DENSE_RANK() OVER (ORDER BY salary DESC) AS salary_rank
FROM employees;

EXPLAIN
SELECT department_id, AVG(salary) AS avg_salary
FROM employees
GROUP BY department_id;

EXPLAIN
SELECT e.emp_id, e.emp_name, d.dept_name, e.salary
FROM employees e
JOIN departments d ON e.department_id = d.dept_id;

EXPLAIN
SELECT d.dept_name, SUM(o.amount) AS total_revenue
FROM departments d
JOIN employees e ON d.dept_id = e.department_id
JOIN orders o ON e.emp_id = o.emp_id
GROUP BY d.dept_name;