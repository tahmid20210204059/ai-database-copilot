# Finance Domain Few-Shot Examples


## Purpose

This document provides finance-focused examples to help the Text-to-SQL engine understand financial business questions and translate them into accurate SQL queries.


The examples cover:

- Revenue analysis
- Payments
- Invoices
- Outstanding balances
- Expenses
- Profit analysis
- Financial summaries
- Transaction analysis


The AI must learn the business interpretation pattern.

Do not copy SQL blindly.

Always adapt queries according to the actual database schema.



==================================================
FINANCE ENTITY UNDERSTANDING
==================================================


Common Finance Entities:


Invoice

Possible tables:

- invoices
- bills
- transactions



Payment

Possible tables:

- payments
- receipts
- settlements



Revenue

Possible tables:

- sales
- orders
- transactions



Expense

Possible tables:

- expenses
- costs
- purchases



Balance

Possible tables:

- accounts
- payments
- invoices



==================================================
EXAMPLE 1: TOTAL REVENUE
==================================================


User Request:

How much revenue did we generate?


Business Intent:

Calculate total business income.



Possible Schema:


sales_orders:

id

total_amount



Expected Interpretation:


Revenue usually comes from:

- sales amount
- order amount
- transaction value



SQL Pattern:


SELECT

SUM(total_amount) AS total_revenue

FROM sales_orders;



Important Rules:

- Use available financial amount fields.
- Never invent revenue columns.



==================================================
EXAMPLE 2: MONTHLY REVENUE
==================================================


User Request:

Show monthly revenue this year.


Business Intent:

Analyze revenue trend by month.



Possible Schema:


sales_orders:

total_amount

order_date



Expected Logic:


Need:

- Date filtering
- Year extraction
- Monthly grouping
- Revenue aggregation



SQL Pattern:


SELECT

YEAR(order_date) AS year,

MONTH(order_date) AS month,

SUM(total_amount) AS revenue


FROM sales_orders


WHERE YEAR(order_date)=YEAR(CURDATE())


GROUP BY

YEAR(order_date),

MONTH(order_date);



Important Rules:

Use available date fields only.



==================================================
EXAMPLE 3: TOP CUSTOMERS BY REVENUE
==================================================


User Request:

Which customers generated the most revenue?


Business Intent:

Rank customers by financial contribution.



Possible Schema:


customers:

id

company_name


sales_orders:

customer_id

total_amount



Expected Logic:


Relationship:


customers.id

↓

sales_orders.customer_id



SQL Pattern:


SELECT


c.company_name,

SUM(so.total_amount) AS revenue


FROM customers c


JOIN sales_orders so

ON c.id=so.customer_id


GROUP BY c.company_name


ORDER BY revenue DESC


LIMIT 10;



Important Rules:

- Ranking requires ORDER BY.
- Revenue requires a financial measure.
- Customer ranking requires customer relationship.



==================================================
EXAMPLE 4: UNPAID INVOICES
==================================================


User Request:

Show unpaid invoices.


Business Intent:

Find invoices that have not been fully paid.



Possible Schema:


invoices:

id

invoice_number

status

amount



Expected Logic:


Filter unpaid status.



SQL Pattern:


SELECT

invoice_number,

amount


FROM invoices


WHERE status='unpaid';



Important Rules:

Use actual payment status fields.



==================================================
EXAMPLE 5: OUTSTANDING BALANCE
==================================================


User Request:

Show customers with outstanding balances.


Business Intent:

Find customers who still owe money.



Possible Schema:


customers:

id

company_name


invoices:

customer_id

amount

paid_amount



Expected Logic:


Calculate remaining balance.


Formula:


amount - paid_amount



SQL Pattern:


SELECT

c.company_name,

SUM(i.amount - i.paid_amount) AS outstanding_balance


FROM customers c


JOIN invoices i

ON c.id=i.customer_id


GROUP BY c.company_name;



Important Rules:

Only calculate fields that exist.

Handle NULL values when required.



==================================================
EXAMPLE 6: HIGHEST VALUE INVOICES
==================================================


User Request:

Show the largest invoices.


Business Intent:

Rank invoices by amount.



Schema:


invoices:

invoice_number

amount



SQL Pattern:


SELECT

invoice_number,

amount


FROM invoices


ORDER BY amount DESC


LIMIT 10;



Important Rules:

Words like:

largest

highest

biggest

mean ranking.



==================================================
EXAMPLE 7: PAYMENT SUMMARY
==================================================


User Request:

Show total payments received.


Business Intent:

Calculate received money.



Schema:


payments:

amount



SQL Pattern:


SELECT

SUM(amount) AS total_received


FROM payments;



Important Rules:

Payment and revenue are not always the same.

Use payment tables for received money.



==================================================
EXAMPLE 8: PAYMENT METHOD ANALYSIS
==================================================


User Request:

Which payment methods are used most?


Business Intent:

Analyze payment preferences.



Schema:


payments:

payment_method

id



SQL Pattern:


SELECT

payment_method,

COUNT(id) AS usage_count


FROM payments


GROUP BY payment_method


ORDER BY usage_count DESC;



Important Rules:

Use COUNT for frequency questions.



==================================================
EXAMPLE 9: RECENT TRANSACTIONS
==================================================


User Request:

Show transactions from the last 30 days.


Business Intent:

Time-based financial filtering.



Schema:


transactions:

transaction_date



SQL Pattern:


SELECT *

FROM transactions


WHERE transaction_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY);



Important Rules:

Understand natural date language.



==================================================
EXAMPLE 10: PROFIT ANALYSIS
==================================================


User Request:

Show products generating the highest profit.


Business Intent:

Rank products by profit.



Possible Schema:


products:

id


order_items:

product_id

selling_price

cost_price



Expected Logic:


Profit:

selling_price - cost_price



SQL Pattern:


Calculate profit only if required fields exist.



Important Rules:

Never assume profit exists.

Use available cost and sales fields.



==================================================
EXAMPLE 11: AVERAGE ORDER VALUE
==================================================


User Request:

What is the average order value?


Business Intent:

Calculate average transaction size.



Schema:


orders:

total_amount



SQL Pattern:


SELECT

AVG(total_amount) AS average_order_value


FROM orders;



Important Rules:

Average questions use AVG.



==================================================
EXAMPLE 12: CUSTOMERS WITH HIGH SPENDING
==================================================


User Request:

Find customers who spent more than 10000.


Business Intent:

Filter aggregated customer spending.



Schema:


customers

orders



SQL Pattern:


SELECT

c.company_name,

SUM(o.total_amount) AS spending


FROM customers c


JOIN orders o

ON c.id=o.customer_id


GROUP BY c.company_name


HAVING SUM(o.total_amount) > 10000;



Important Rules:

Use HAVING for aggregated conditions.



==================================================
EXAMPLE 13: YEARLY FINANCIAL SUMMARY
==================================================


User Request:

Show yearly sales performance.


Business Intent:

Compare yearly revenue.



Schema:


sales_orders:

order_date

total_amount



SQL Pattern:


SELECT

YEAR(order_date),

SUM(total_amount)


FROM sales_orders


GROUP BY YEAR(order_date);



==================================================
EXAMPLE 14: FAILED OR CANCELLED PAYMENTS
==================================================


User Request:

Show failed payments.


Business Intent:

Filter payment failures.



Schema:


payments:

status



SQL Pattern:


SELECT *

FROM payments


WHERE status='failed';



==================================================
EXAMPLE 15: FINANCIAL DASHBOARD SUMMARY
==================================================


User Request:

Give me a financial overview.


Business Intent:


Provide summary metrics.


Possible metrics:


- Total revenue
- Total payments
- Total transactions
- Average order value



Important Rules:


Choose only metrics available in schema.

Do not invent financial indicators.



==================================================
FINANCE VALIDATION RULES
==================================================


Before generating finance queries:


✓ Identify correct financial entity.

✓ Distinguish revenue from payment.

✓ Distinguish invoice from transaction.

✓ Use correct financial measurement.

✓ Use SUM for totals.

✓ Use AVG for averages.

✓ Use COUNT for quantities.

✓ Use HAVING for aggregated filters.

✓ Use date columns correctly.

✓ Never invent financial fields.



==================================================
FINANCE BUSINESS PRINCIPLE
==================================================


Every finance question should answer:


What money?

(Revenue, payment, expense, balance)


From where?

(Customer, order, invoice, transaction)


When?

(Date period)


How much?

(SUM, COUNT, AVG)


Then generate SQL.