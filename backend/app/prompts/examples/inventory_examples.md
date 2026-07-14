# Inventory Domain Few-Shot Examples


## Purpose

This document provides inventory-focused examples to help the Text-to-SQL engine understand warehouse, stock, product availability, and inventory management questions.


The examples teach the AI how to map:

- Inventory business questions
- Product entities
- Warehouse concepts
- Stock metrics
- Supplier relationships
- Inventory movement


The AI must understand the business meaning first and then generate SQL based on the available schema.

Never copy SQL blindly.

Always adapt to the provided database schema.



==================================================
INVENTORY ENTITY UNDERSTANDING
==================================================


Common Inventory Entities:


Product

Possible tables:

- products
- items
- inventory_items
- catalog



Inventory

Possible tables:

- inventory
- stock
- warehouse_stock
- inventory_levels



Warehouse

Possible tables:

- warehouses
- locations
- storage



Supplier

Possible tables:

- suppliers
- vendors
- manufacturers



Inventory Transaction

Possible tables:

- stock_movements
- inventory_transactions
- transactions



==================================================
EXAMPLE 1: SHOW ALL PRODUCTS
==================================================


User Request:

Show all products.


Business Intent:

Retrieve product catalog information.



Possible Schema:


products:

id

product_name

sku

category_id

selling_price



Expected SQL Pattern:


SELECT

product_name,

sku,

selling_price


FROM products;



Important Rules:

- Use product display fields.
- Avoid returning technical IDs unless requested.



==================================================
EXAMPLE 2: PRODUCT DETAILS
==================================================


User Request:

Show product names and prices.


Business Intent:

Display product information.



Schema:


products:

product_name

selling_price



Expected SQL Pattern:


SELECT

product_name,

selling_price


FROM products;



Important Rules:

Choose business-readable columns.



==================================================
EXAMPLE 3: LOW STOCK PRODUCTS
==================================================


User Request:

Which products are running low?


Business Intent:

Find products requiring restocking.



Possible Schema:


products:

id

product_name


inventory:

product_id

quantity_on_hand

reorder_level



Expected Relationship:


products.id

↓

inventory.product_id



SQL Pattern:


SELECT

p.product_name,

i.quantity_on_hand


FROM products p


JOIN inventory i

ON p.id=i.product_id


WHERE i.quantity_on_hand < i.reorder_level;



Important Rules:

Low stock usually means:

available quantity is below reorder threshold.



==================================================
EXAMPLE 4: PRODUCTS WITH AVAILABLE STOCK
==================================================


User Request:

Show products currently available.


Business Intent:

Find products with inventory availability.



Schema:


products:

product_name


inventory:

quantity_on_hand



Expected Logic:


Filter positive inventory quantity.



SQL Pattern:


SELECT

p.product_name,

i.quantity_on_hand


FROM products p


JOIN inventory i

ON p.id=i.product_id


WHERE i.quantity_on_hand > 0;



==================================================
EXAMPLE 5: TOP SELLING PRODUCTS
==================================================


User Request:

Which products sell the most?


Business Intent:

Rank products by sales performance.



Possible Schema:


products:

id

product_name


order_items:

product_id

quantity



Expected Relationship:


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

Selling performance requires:

- Sales table
- Order items
- Quantity or revenue metric



==================================================
EXAMPLE 6: PRODUCTS BY REVENUE
==================================================


User Request:

Show products generating the highest revenue.


Business Intent:

Rank products by money generated.



Schema:


products:

id

product_name


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

Use revenue fields when available.

Do not use quantity if user asks revenue.



==================================================
EXAMPLE 7: INVENTORY BY WAREHOUSE
==================================================


User Request:

Show stock levels by warehouse.


Business Intent:

Analyze inventory distribution.



Schema:


warehouses:

id

warehouse_name


inventory:

warehouse_id

quantity_on_hand



Relationship:


warehouses.id

↓

inventory.warehouse_id



SQL Pattern:


SELECT

w.warehouse_name,

SUM(i.quantity_on_hand) AS stock


FROM warehouses w


JOIN inventory i

ON w.id=i.warehouse_id


GROUP BY w.warehouse_name;



==================================================
EXAMPLE 8: LOW INVENTORY BY WAREHOUSE
==================================================


User Request:

Which warehouses have low stock?


Business Intent:

Find warehouse inventory problems.



Expected Logic:


Aggregate stock by warehouse.

Compare against available threshold if schema provides one.



Important Rules:

Never invent warehouse limits.



==================================================
EXAMPLE 9: PRODUCT CATEGORY ANALYSIS
==================================================


User Request:

Show sales by product category.


Business Intent:

Analyze category performance.



Schema:


products:

category_id


categories:

id

category_name


order_items:

product_id

line_total



Relationship:


categories

↓

products

↓

order_items



SQL Pattern:


SELECT

c.category_name,

SUM(oi.line_total) AS sales


FROM categories c


JOIN products p

ON c.id=p.category_id


JOIN order_items oi

ON p.id=oi.product_id


GROUP BY c.category_name;



==================================================
EXAMPLE 10: PRODUCTS NEVER SOLD
==================================================


User Request:

Show products that have never been sold.


Business Intent:

Find inactive products.



Schema:


products

order_items



Expected Logic:


Use LEFT JOIN.

Find missing sales records.



SQL Pattern:


SELECT

p.product_name


FROM products p


LEFT JOIN order_items oi

ON p.id=oi.product_id


WHERE oi.id IS NULL;



==================================================
EXAMPLE 11: INVENTORY VALUE
==================================================


User Request:

What is the total inventory value?


Business Intent:

Calculate stock worth.



Possible Schema:


inventory:

quantity_on_hand


products:

selling_price



Logic:


Inventory value:

quantity × price



SQL Pattern:


Calculate only if required columns exist.



Important Rules:

Do not calculate financial values without supporting columns.



==================================================
EXAMPLE 12: SUPPLIER PRODUCT LIST
==================================================


User Request:

Show products supplied by each supplier.


Business Intent:

Connect suppliers and products.



Schema:


suppliers:

id

supplier_name


products:

supplier_id

product_name



Relationship:


suppliers.id

↓

products.supplier_id



SQL Pattern:


SELECT

s.supplier_name,

p.product_name


FROM suppliers s


JOIN products p

ON s.id=p.supplier_id;



==================================================
EXAMPLE 13: PRODUCT SEARCH
==================================================


User Request:

Find products containing "phone".


Business Intent:

Search product catalog.



Schema:


products:

product_name



SQL Pattern:


SELECT *

FROM products


WHERE product_name LIKE '%phone%';



Important Rules:

Use available text columns only.



==================================================
EXAMPLE 14: STOCK MOVEMENT ANALYSIS
==================================================


User Request:

Show stock changes over time.


Business Intent:

Analyze inventory movement trends.



Possible Schema:


inventory_transactions:

product_id

quantity

created_at



Expected Logic:


Use:

- Date grouping
- Quantity changes



==================================================
EXAMPLE 15: INVENTORY SUMMARY
==================================================


User Request:

Give me an inventory overview.


Business Intent:

Provide inventory statistics.



Possible Metrics:


- Total products
- Available stock
- Low stock items
- Warehouse distribution



Important Rules:

Use only available schema metrics.



==================================================
INVENTORY VALIDATION RULES
==================================================


Before generating inventory queries:


✓ Identify product entity correctly.

✓ Distinguish product from inventory record.

✓ Use inventory tables for stock questions.

✓ Use sales tables for selling performance.

✓ Use warehouse relationships correctly.

✓ Use quantity fields appropriately.

✓ Use SUM for total stock.

✓ Use COUNT for product quantity.

✓ Use ORDER BY for ranking.

✓ Never invent stock thresholds.



==================================================
INVENTORY BUSINESS PRINCIPLE
==================================================


Every inventory question should answer:


What item?

(Product)


Where?

(Warehouse)


How many?

(Quantity)


How valuable?

(Value)


How moving?

(Sales/Transactions)


Then generate SQL.