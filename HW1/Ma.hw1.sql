# use employees;

# select dept_name, dept_no
# FROM departments;

# Q1 Write SQL Code to count the number of employees – 1 pts
SELECT COUNT(*) FROM employees;
# 300024

# Q2 Write SQL Code to output the current name of all of the departments -2 pts
SELECT dept_name FROM departments;
# Customer Service, Development, Finance, Human Resources, Marketing, Production, Quality Management, Research, Sales

# Q3 How many employees are in Finance? -2 pts
SELECT COUNT(*) FROM dept_emp WHERE dept_no = 'd002';
# 17346

# Q4 How many women work in development? – 3 pts
SELECT COUNT(*) FROM dept_emp INNER JOIN employees
ON dept_emp.emp_no = employees.emp_no WHERE employees.gender = 'F';
#132753

# Q5 What is the top salary in the company? 3 pts
SELECT salary FROM salaries ORDER BY salary DESC LIMIT 1;
#158220

# Q6 What is the average salary for Marketing? 4 pts
SELECT AVG(salary) FROM salaries
INNER JOIN employees ON salaries.emp_no = employees.emp_no
INNER JOIN dept_emp ON employees.emp_no = dept_emp.emp_no
WHERE dept_no = "d001";
# 71913.2

# Q7 What is the lowest salary in the company, who is it and what is their title and department? 5 pts
SELECT first_name, last_name, salary, titles.title, departments.dept_name
FROM employees
JOIN salaries ON employees.emp_no = salaries.emp_no
JOIN titles ON employees.emp_no = titles.emp_no
JOIN dept_emp ON employees.emp_no = dept_emp.emp_no
JOIN departments ON dept_emp.dept_no = departments.dept_no
ORDER BY salary
LIMIT 1;
# Olivera | Baek | 38623 | Technique Leader | Production

# Q8 Who is the oldest person at the company and what is their age? 5 pts
SELECT first_name, last_name, birth_date, DATEDIFF(NOW(), birth_date) / 365 AS age
FROM employees
ORDER BY birth_date
LIMIT 1;
# Jouni | Pocchiola | 1952-02-1 | 71.0603
