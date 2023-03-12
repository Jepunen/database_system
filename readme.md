Jere Puurunen - 0607312
Jericho Koskinen - 0607024

Queries used in the project:

'''
SELECT
    employee_id as 'ID', name as 'Name', email as 'Email', salary as 'Salary (€)'
FROM 
    employees;
'''

'''
SELECT
    order_id as 'Order ID', customer_id as 'Customer ID', order_date as 'Order date', total_cost as 'Total cost'
FROM
    orders
WHERE
    total_cost > 50;
'''

'''
SELECT
    order_id as 'Order ID', order_date as 'Date', total_cost as 'Total (€)'
FROM
    Orders WHERE Order_Date='20200101';'
'''

'''
SELECT
    employees.name, employee_roles.role
FROM
    employees
INNER JOIN
    employee_roles ON employees.employee_id = employee_roles.employee_id;
'''

'''
SELECT
    customers.name as 'Name', orders.order_id as 'Order ID', orders.total_cost as 'Total cost', products.name as 'Product', order_details.quantity as 'Quantity'
FROM
    customers
INNER JOIN
    orders ON customers.customer_id = orders.customer_id
INNER JOIN
    order_details ON orders.order_id = order_details.order_id
INNER JOIN
    products ON order_details.product_id = products.product_id;
'''