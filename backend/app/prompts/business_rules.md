# Enterprise Business Language Understanding Rules


## Purpose

This document defines how the AI should understand human business language and map it to database concepts.

Users may describe business problems using natural language instead of technical database terms.

The AI must understand:

- Business terminology
- Common synonyms
- Industry language
- Entity meaning
- Metric meaning
- User intent


Never match words only.

Always understand the business meaning behind the request.



==================================================
GENERAL BUSINESS LANGUAGE PRINCIPLES
==================================================


Users may use different words to describe the same business concept.


Example:


User:

"Who are our best clients?"


Possible meaning:

Top customers based on revenue, sales, orders, or another business metric.


The AI must identify the most appropriate interpretation using:

- Schema information
- Available metrics
- Relationships
- Business context



==================================================
CUSTOMER / CLIENT DOMAIN
==================================================


## Customer Synonyms


A customer may be described as:


- customer
- client
- buyer
- purchaser
- consumer
- account
- account holder
- organization
- company
- business
- partner
- subscriber
- member



## Customer Entity Interpretation


Customer can represent:


### Individual Customer

Possible fields:


- customer_name
- full_name
- name
- contact_name
- first_name
- last_name



### Business Customer

Possible fields:


- company_name
- organization_name
- business_name
- account_name



Choose based on user intent.


Examples:


User:

"Show customer names"


Prefer:

contact_name


User:

"Show customer companies"


Prefer:

company_name


User:

"List business customers"


Prefer:

company_name



==================================================
PRODUCT / ITEM DOMAIN
==================================================


## Product Synonyms


Product may mean:


- product
- item
- goods
- merchandise
- article
- SKU
- stock item
- inventory item
- catalog item
- offering



## Product Identification


Prefer:


Product display:

- product_name
- item_name
- name


Product identifier:

- product_id
- sku
- product_code



Examples:


User:

"Best selling products"


Look for:

- product
- order_items
- sales quantity
- sales amount



User:

"Products running low"


Look for:

- inventory
- stock quantity
- available quantity



==================================================
SALES DOMAIN
==================================================


## Sales Synonyms


Sales may mean:


- sales
- revenue
- income
- turnover
- earnings
- gross sales
- net sales
- sales amount
- transaction value
- business volume



## Sales Metrics


Possible measurements:


Revenue:

- SUM(total_amount)
- SUM(revenue)


Number of sales:

- COUNT(order_id)
- COUNT(transaction_id)


Average sale:

- AVG(order_amount)



Never assume a metric.

Use schema evidence.



==================================================
ORDER DOMAIN
==================================================


## Order Synonyms


Order may mean:


- order
- purchase
- transaction
- sale
- invoice
- receipt
- bill
- booking
- request
- sales order



## Order Related Concepts


Order value:

- total_amount
- order_total
- amount


Order date:

- order_date
- created_at
- transaction_date


Order status:

- status
- order_status



==================================================
PAYMENT / FINANCE DOMAIN
==================================================


## Payment Synonyms


Payment may mean:


- payment
- transaction
- receipt
- collection
- settlement
- deposit
- transfer
- invoice payment



## Finance Metrics


Revenue:

- sales amount
- total amount
- income


Outstanding:

- unpaid amount
- balance
- due amount


Profit:

- revenue - cost
- margin


Never calculate unavailable metrics.



==================================================
INVENTORY DOMAIN
==================================================


## Inventory Synonyms


Inventory may mean:


- stock
- warehouse stock
- available stock
- quantity
- items available
- inventory level
- stock level
- availability



## Inventory Metrics


Stock quantity:

- quantity
- quantity_on_hand
- available_quantity


Reserved stock:

- quantity_reserved


Low stock:

Compare:

quantity_on_hand

against:

reorder_level



Examples:


User:

"Which products are low in stock?"


Look for:

products

+

inventory

+

quantity fields



==================================================
WAREHOUSE DOMAIN
==================================================


## Warehouse Synonyms


Warehouse may mean:


- warehouse
- storage
- location
- distribution center
- depot
- facility



Possible fields:


- warehouse_name
- location
- city
- address



==================================================
SUPPLIER / VENDOR DOMAIN
==================================================


## Supplier Synonyms


Supplier may mean:


- supplier
- vendor
- manufacturer
- provider
- distributor
- source



Possible fields:


- supplier_name
- vendor_name
- company_name



==================================================
EMPLOYEE / HR DOMAIN
==================================================


## Employee Synonyms


Employee may mean:


- employee
- staff
- worker
- team member
- representative
- salesperson
- executive
- agent
- manager



## Employee Display Fields


Prefer:


- employee_name
- full_name
- first_name + last_name



## Employee Business Roles


Salesperson:

- sales_employee
- representative
- agent


Manager:

- manager
- supervisor
- team lead



==================================================
DEPARTMENT DOMAIN
==================================================


Department may mean:


- department
- division
- team
- unit
- business function



Examples:


HR department

Sales department

Finance department



==================================================
CRM DOMAIN
==================================================


## Lead Synonyms


Lead may mean:


- prospect
- potential customer
- opportunity
- inquiry
- contact



## Opportunity Synonyms


Opportunity may mean:


- deal
- sales opportunity
- pipeline item
- potential sale



## Account Synonyms


Account may mean:


- customer account
- business customer
- organization



==================================================
TIME AND DATE BUSINESS LANGUAGE
==================================================


Understand:


Today:

Current date


Yesterday:

Previous day


This week:

Current week range


Last week:

Previous week range


This month:

Current month


Last month:

Previous month


This quarter:

Current quarter


Last quarter:

Previous quarter


This year:

Current year


Last year:

Previous year


Past 30 days:

DATE_SUB(CURDATE(), INTERVAL 30 DAY)


Past 90 days:

DATE_SUB(CURDATE(), INTERVAL 90 DAY)



==================================================
RANKING LANGUAGE
==================================================


Ranking words:


- top
- highest
- best
- largest
- biggest
- strongest
- leading
- most valuable
- most profitable


Usually implies:


ORDER BY DESC

+

LIMIT



Opposite:


- lowest
- smallest
- weakest
- least


Usually implies:


ORDER BY ASC



==================================================
COMPARISON LANGUAGE
==================================================


Comparison words:


- compare
- difference
- versus
- vs
- between
- growth
- change


May require:


- grouping
- aggregation
- calculated differences



==================================================
AGGREGATION LANGUAGE
==================================================


Total:


COUNT

SUM


Average:


AVG


Maximum:


MAX


Minimum:


MIN


Number of:


COUNT



==================================================
BUSINESS INTENT EXAMPLES
==================================================


User:

"Who are the best customers?"


Interpretation:

Find customer ranking using the most appropriate business metric.



User:

"Which products sell the most?"


Interpretation:

Rank products using sales quantity or revenue.



User:

"Which employees perform best?"


Interpretation:

Rank employees using available performance metrics.



User:

"Which items need restocking?"


Interpretation:

Find inventory items below stock threshold.



==================================================
AMBIGUITY HANDLING RULES
==================================================


When a business word has multiple meanings:


Example:

"Customer"


Could mean:

- Person
- Company
- Account


Choose using:


1. User wording

2. Schema meaning

3. Available relationships

4. Available display columns


Do not randomly choose fields.



==================================================
FINAL BUSINESS RULE
==================================================


Understand the user's business goal first.

Map business language to database meaning second.

Generate SQL only after the correct business interpretation is identified.