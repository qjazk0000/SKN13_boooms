use test_db;

CREATE TABLE Employees (
id INT PRIMARY KEY,
name VARCHAR(50),
salary DECIMAL(10, 2),
department VARCHAR(50)
);

INSERT INTO Employees (id, name, salary, department) VALUES
(1, 'Alice', 5000.00, 'HR'),
(2, 'Bob', NULL, 'Finance'),
(3, 'Charlie', 7000.00, 'IT'),
(4, 'David', NULL, 'IT');

select * from Employees;

-- NULL값 다루기
select name, ifnull(salary, "무료 봉사") as "IFNULL 결과"
from Employees;