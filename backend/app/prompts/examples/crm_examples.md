# CRM Domain Few-Shot Examples

## Purpose

This document provides CRM-focused examples to help the Text-to-SQL engine understand common customer relationship management questions.

These examples teach the AI how to map:

- Human business language
- CRM concepts
- Database entities
- Relationships
- Metrics
- SQL patterns


The AI should learn the reasoning pattern, not copy SQL blindly.

Always adapt queries according to the actual provided schema.



==================================================
CRM ENTITY UNDERSTANDING
==================================================


Common CRM entities:


Customer

Possible tables:

- customers
- clients
- accounts
- organizations



Contact Person

Possible tables:

- contacts
- customer_contacts
- customer_details



Lead

Possible tables:

- leads
- prospects
- opportunities



Opportunity

Possible tables:

- opportunities
- deals
- pipeline



Interaction

Possible tables:

- activities
- communications
- calls
- meetings



==================================================
EXAMPLE 1: CUSTOMER LIST
==================================================


User Request:

Show all customers.



Business Intent:

Retrieve the customer master list.



Schema Example:


customers

Columns:

id

company_name

contact_name

email

status



SQL Pattern:


SELECT

customer display fields

FROM customers;



Important Rules:

- Use customer display columns.
- Avoid technical IDs unless requested.
- Return meaningful business information.



==================================================
EXAMPLE 2: CUSTOMER CONTACT INFORMATION
==================================================


User Request:

Show customer names and contact details.



Business Intent:

Display human contact information.



Schema Example:


customers:

id

company_name

contact_name

email

phone



Expected Interpretation:


Customer name means:

contact_name


Not:

company_name


SQL Pattern:


SELECT

contact_name,

email,

phone

FROM customers;



Important Rules:

Choose human-readable contact fields when user asks for names.



==================================================
EXAMPLE 3: BUSINESS CUSTOMER COMPANIES
==================================================


User Request:

Show customer companies.



Business Intent:

Display organization names.



Schema Example:


customers:

company_name

contact_name



Expected Interpretation:


Use:

company_name



SQL Pattern:


SELECT

company_name

FROM customers;



Important Rules:

Company/business wording indicates organization fields.



==================================================
EXAMPLE 4: ACTIVE CUSTOMERS
==================================================


User Request:

Show active customers.



Business Intent:

Filter customers based on account status.



Schema Example:


customers:

id

company_name

status



Expected SQL Pattern:


SELECT

company_name

FROM customers

WHERE status='active';



Important Rules:

Use available status columns only.



==================================================
EXAMPLE 5: CUSTOMER COUNT
==================================================


User Request:

How many customers do we have?



Business Intent:

Count customer records.



Schema Example:


customers:

id



Expected SQL Pattern:


SELECT

COUNT(id)

FROM customers;



Important Rules:

Use COUNT for quantity questions.



==================================================
EXAMPLE 6: TOP CUSTOMERS BY SALES
==================================================


User Request:

Who are the top customers by sales?



Business Intent:

Rank customers using sales value.



Possible Schema:


customers:

id

company_name



sales_orders:

customer_id

total_amount



Expected Interpretation:


Need:

customers

+

sales_orders


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

ON c.id = so.customer_id


GROUP BY c.company_name


ORDER BY total_sales DESC


LIMIT 10;



Important Rules:

- Ranking requires ordering.
- Sales requires a financial measure.
- Use SUM when total amount exists.



==================================================
EXAMPLE 7: CUSTOMERS WITH NO PURCHASES
==================================================


User Request:

Show customers who have never purchased anything.



Business Intent:

Find customers without transactions.



Possible Schema:


customers

orders



Expected Logic:


Need:

LEFT JOIN


Find missing orders.


SQL Pattern:


SELECT

c.company_name


FROM customers c


LEFT JOIN orders o

ON c.id=o.customer_id


WHERE o.id IS NULL;



Important Rules:

Use existence checks carefully.



==================================================
EXAMPLE 8: RECENTLY INACTIVE CUSTOMERS
==================================================


User Request:

Show customers who have not ordered recently.



Business Intent:

Find inactive customers.



Possible Schema:


customers

orders

order_date



Expected Logic:


Find customers with no recent orders.



Possible SQL Pattern:


Use:

LEFT JOIN

DATE filtering

NULL check



Important Rules:

Understand "inactive" as missing recent activity.



==================================================
EXAMPLE 9: CUSTOMER REVENUE SUMMARY
==================================================


User Request:

Show revenue generated by each customer.



Business Intent:

Customer-level revenue analytics.



Schema:


customers

sales_orders



Expected Logic:


Customer:

GROUP BY customer


Revenue:

SUM(total_amount)



SQL Pattern:


SELECT

c.company_name,

SUM(so.total_amount) AS revenue


FROM customers c


JOIN sales_orders so

ON c.id=so.customer_id


GROUP BY c.company_name;



==================================================
EXAMPLE 10: HIGH VALUE CUSTOMERS
==================================================


User Request:

Find customers who spent more than 10000.



Business Intent:

Filter customers based on aggregated sales.



Expected Logic:


Use:

GROUP BY

HAVING



SQL Pattern:


SELECT

c.company_name,

SUM(so.total_amount) AS total_spent


FROM customers c


JOIN sales_orders so

ON c.id=so.customer_id


GROUP BY c.company_name


HAVING SUM(so.total_amount) > 10000;



Important Rules:

Aggregate filtering uses HAVING, not WHERE.



==================================================
EXAMPLE 11: CUSTOMER BY REGION
==================================================


User Request:

Show customers by region.



Business Intent:

Group customers geographically.



Schema:


customers:

company_name

region



SQL Pattern:


SELECT

region,

COUNT(id)


FROM customers


GROUP BY region;



==================================================
EXAMPLE 12: CUSTOMER GROWTH TREND
==================================================


User Request:

Show new customers each month.



Business Intent:

Time-based customer acquisition analysis.



Schema:


customers:

created_at



Expected Logic:


Group by:

year

month



SQL Pattern:


SELECT

YEAR(created_at),

MONTH(created_at),

COUNT(id)


FROM customers


GROUP BY

YEAR(created_at),

MONTH(created_at);



==================================================
CRM VALIDATION RULES
==================================================


Before generating CRM queries:


✓ Identify customer entity correctly.

✓ Separate person name from company name.

✓ Use correct customer relationships.

✓ Use sales/orders tables for revenue questions.

✓ Use aggregation for ranking.

✓ Use HAVING for aggregate filters.

✓ Avoid assuming CRM terminology.

✓ Use schema evidence first.



==================================================
CRM BUSINESS PRINCIPLE
==================================================


A CRM query should answer a business question.

Always think:

Who?

(Customer)

What?

(Activity, purchase, revenue, interaction)

When?

(Date/time)

How much?

(Metric)

Then generate SQL.