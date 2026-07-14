# Sales Domain Few-Shot Examples


## Purpose

This document provides sales-focused examples to help the Text-to-SQL engine understand sales analytics, order management, revenue calculation, customer purchasing behavior, and sales performance questions.


These examples teach the AI how to map:

- Business sales questions
- Customer transactions
- Orders
- Revenue metrics
- Sales representatives
- Product performance
- Regional performance


The AI must understand the business meaning first and then generate SQL according to the available schema.

Never copy SQL blindly.

Always adapt queries based on the actual database structure.



==================================================
SALES ENTITY UNDERSTANDING
==================================================


Common Sales Entities:


Customer

Possible tables:

- customers
- clients
- accounts



Sales Order

Possible tables:

- sales_orders
- orders
- transactions



Order Item

Possible tables:

- order_items
- order_details
- sales_details



Payment

Possible tables:

- payments
- receipts



Sales Employee

Possible tables:

- employees
- sales_representatives
- agents



Product

Possible tables:

- products
- items



==================================================
EXAMPLE 1: TOTAL SALES
==================================================


User Request:

How much total sales did we make?


Business Intent:

Calculate total sales revenue.



Possible Schema:


sales_orders:

id

total_amount



Expected Interpretation:


Sales amount is stored in:

total_amount



SQL Pattern:


SELECT

SUM(total_amount) AS total_sales


FROM sales_orders;



Important Rules:

- Use financial amount fields.
- Do not confuse sales with payment unless requested.



==================================================
EXAMPLE 2: SALES BY CUSTOMER
==================================================


User Request:

Show sales by customer.


Business Intent:

Calculate customer-level sales performance.



Schema:


customers:

id

company_name


sales_orders:

customer_id

total_amount



Relationship:


customers.id

↓

sales_orders.customer_id



SQL Pattern:


SELECT

c.company_name,

SUM(so.total_amount) AS total_sales


FROM customers c


JOIN sales_orders so

ON c.id=so.customer_id


GROUP BY c.company_name;



Important Rules:

Customer analytics require customer-sales relationships.



==================================================
EXAMPLE 3: TOP CUSTOMERS BY SALES
==================================================


User Request:

Show the top 10 customers by sales.


Business Intent:

Rank customers by revenue contribution.



Schema:


customers:

id

company_name


sales_orders:

customer_id

total_amount



SQL Pattern:


SELECT

c.company_name,

SUM(so.total_amount) AS total_sales


FROM customers c


JOIN sales_orders so

ON c.id=so.customer_id


GROUP BY c.company_name


ORDER BY total_sales DESC


LIMIT 10;



Important Rules:

Ranking requires:

- Aggregation
- ORDER BY DESC
- LIMIT



==================================================
EXAMPLE 4: CUSTOMER PURCHASE FREQUENCY
==================================================


User Request:

Which customers place the most orders?


Business Intent:

Rank customers by number of transactions.



Schema:


customers:

id

company_name


sales_orders:

customer_id

id



SQL Pattern:


SELECT

c.company_name,

COUNT(so.id) AS order_count


FROM customers c


JOIN sales_orders so

ON c.id=so.customer_id


GROUP BY c.company_name


ORDER BY order_count DESC


LIMIT 10;



Important Rules:

"Most orders" means COUNT.

Not SUM.



==================================================
EXAMPLE 5: MONTHLY SALES TREND
==================================================


User Request:

Show monthly sales trend.


Business Intent:

Analyze sales performance over time.



Schema:


sales_orders:

order_date

total_amount



SQL Pattern:


SELECT

YEAR(order_date) AS year,

MONTH(order_date) AS month,

SUM(total_amount) AS sales


FROM sales_orders


GROUP BY

YEAR(order_date),

MONTH(order_date)


ORDER BY year, month;



Important Rules:

Time analysis requires date fields.



==================================================
EXAMPLE 6: SALES THIS YEAR
==================================================


User Request:

Show sales this year.


Business Intent:

Filter sales records for current year.



Schema:


sales_orders:

order_date

total_amount



SQL Pattern:


SELECT

SUM(total_amount) AS sales


FROM sales_orders


WHERE YEAR(order_date)=YEAR(CURDATE());



Important Rules:

Use date functions only when date columns exist.



==================================================
EXAMPLE 7: RECENT SALES
==================================================


User Request:

Show sales from the last 30 days.


Business Intent:

Recent sales analysis.



SQL Pattern:


SELECT *

FROM sales_orders


WHERE order_date >= DATE_SUB(
CURDATE(),
INTERVAL 30 DAY
);



Important Rules:

Understand natural time expressions.



==================================================
EXAMPLE 8: BEST SELLING PRODUCTS
==================================================


User Request:

Which products sell the most?


Business Intent:

Rank products based on sales quantity.



Schema:


products:

id

product_name


order_items:

product_id

quantity



Relationship:


products.id

↓

order_items.product_id



SQL Pattern:


SELECT

p.product_name,

SUM(oi.quantity) AS total_sold


FROM products p


JOIN order_items oi

ON p.id=oi.product_id


GROUP BY p.product_name


ORDER BY total_sold DESC


LIMIT 10;



Important Rules:

"Sells most" usually means quantity.

If user says revenue, use amount fields.



==================================================
EXAMPLE 9: PRODUCT SALES REVENUE
==================================================


User Request:

Which products generated the highest revenue?


Business Intent:

Rank products by money generated.



Schema:


products

order_items:

product_id

line_total



SQL Pattern:


SELECT

p.product_name,

SUM(oi.line_total) AS revenue


FROM products p


JOIN order_items oi

ON p.id=oi.product_id


GROUP BY p.product_name


ORDER BY revenue DESC


LIMIT 10;



Important Rules:

Revenue and quantity are different metrics.



==================================================
EXAMPLE 10: SALES BY REGION
==================================================


User Request:

Show sales by region.


Business Intent:

Analyze geographic sales performance.



Schema:


customers:

region


sales_orders:

customer_id

total_amount



SQL Pattern:


SELECT

c.region,

SUM(so.total_amount) AS sales


FROM customers c


JOIN sales_orders so

ON c.id=so.customer_id


GROUP BY c.region;


Important Rules:

Use customer relationship when region belongs to customers.



==================================================
EXAMPLE 11: SALES REPRESENTATIVE PERFORMANCE
==================================================


User Request:

Which sales representatives perform best?


Business Intent:

Rank employees by sales contribution.



Schema:


employees:

id

name


sales_orders:

sales_employee_id

total_amount



SQL Pattern:


SELECT

e.name,

SUM(so.total_amount) AS sales


FROM employees e


JOIN sales_orders so

ON e.id=so.sales_employee_id


GROUP BY e.name


ORDER BY sales DESC


LIMIT 10;



Important Rules:

Performance requires a measurable metric.



==================================================
EXAMPLE 12: AVERAGE ORDER VALUE
==================================================


User Request:

What is the average order value?


Business Intent:

Calculate average transaction size.



Schema:


sales_orders:

total_amount



SQL Pattern:


SELECT

AVG(total_amount) AS average_order_value


FROM sales_orders;



Important Rules:

Average questions use AVG.



==================================================
EXAMPLE 13: CANCELLED SALES
==================================================


User Request:

Show cancelled orders.


Business Intent:

Filter sales by status.



Schema:


sales_orders:

status



SQL Pattern:


SELECT *

FROM sales_orders


WHERE status='cancelled';



Important Rules:

Use available status fields.



==================================================
EXAMPLE 14: HIGH VALUE ORDERS
==================================================


User Request:

Show orders above 50000.


Business Intent:

Filter large transactions.



Schema:


sales_orders:

total_amount



SQL Pattern:


SELECT *

FROM sales_orders


WHERE total_amount > 50000;



==================================================
EXAMPLE 15: CUSTOMER SALES WITHOUT PURCHASES
==================================================


User Request:

Show customers who never purchased.


Business Intent:

Find inactive customers.



Schema:


customers

sales_orders



Logic:


LEFT JOIN

+

NULL check



SQL Pattern:


SELECT

c.company_name


FROM customers c


LEFT JOIN sales_orders so

ON c.id=so.customer_id


WHERE so.id IS NULL;



==================================================
SALES VALIDATION RULES
==================================================


Before generating sales queries:


✓ Identify sales entity correctly.

✓ Separate revenue from payment.

✓ Separate order count from sales amount.

✓ Use correct customer relationships.

✓ Use correct product relationships.

✓ Use SUM for monetary totals.

✓ Use COUNT for transaction frequency.

✓ Use AVG for average metrics.

✓ Use ORDER BY for rankings.

✓ Use GROUP BY correctly.

✓ Use date fields correctly.



==================================================
SALES BUSINESS PRINCIPLE
==================================================


Every sales question should answer:


Who?

(Customer / Employee)


What?

(Product / Order / Transaction)


How much?

(Revenue / Quantity / Profit)


When?

(Date period)


Where?

(Region / Warehouse)


Then generate SQL.