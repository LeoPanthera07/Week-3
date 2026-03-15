CREATE TABLE projects (
    project_id SERIAL PRIMARY KEY,
    project_name VARCHAR(100) NOT NULL,
    lead_emp_id INT REFERENCES employees(emp_id),
    budget NUMERIC(12, 2) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE
);

INSERT INTO projects (project_name, lead_emp_id, budget, start_date, end_date) VALUES
    ('Platform Revamp', 2, 200000, '2024-01-01', '2024-12-31'),
    ('Mobile App', 1, 120000, '2024-02-15', NULL),
    ('Sales Dashboard', 3, 80000, '2024-03-01', '2024-09-30'),
    ('HR Portal', 5, 50000, '2024-04-01', NULL),
    ('Brand Campaign', 6, 90000, '2024-01-10', '2024-06-30');

SELECT e.emp_name, d.dept_name, d.budget AS dept_budget, p.project_name, p.budget AS project_budget
FROM employees e
JOIN projects p ON e.emp_id = p.lead_emp_id
JOIN departments d ON e.department_id = d.dept_id
ORDER BY d.dept_name, e.emp_name, p.project_name;

SELECT d.dept_name, d.budget AS dept_budget, SUM(p.budget) AS total_project_budget
FROM departments d
JOIN employees e ON d.dept_id = e.department_id
JOIN projects p ON e.emp_id = p.lead_emp_id
GROUP BY d.dept_name, d.budget
HAVING SUM(p.budget) > d.budget;