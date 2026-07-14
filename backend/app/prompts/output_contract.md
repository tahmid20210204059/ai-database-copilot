# Enterprise AI SQL Output Contract


## Purpose

This document defines the strict response format required from the AI SQL generation engine.

The AI must return a predictable, machine-readable response that can be safely consumed by backend services and frontend applications.


The output must support:

- SQL execution pipeline
- Query preview UI
- Query history storage
- Confidence display
- Error handling
- Audit tracking



==================================================
STRICT OUTPUT REQUIREMENT
==================================================

Return ONLY valid JSON.

Never return:

- Markdown
- Code blocks
- Explanations outside JSON
- Natural language before JSON
- Natural language after JSON
- Comments
- Trailing commas



The response must be directly parseable by a JSON parser.



==================================================
REQUIRED RESPONSE STRUCTURE
==================================================


Always return exactly:


{
    "sql": "",
    "summary": "",
    "confidence": 0.0,
    "tables_used": [],
    "read_only": true
}



==================================================
FIELD DEFINITIONS
==================================================



## sql


Type:

String



Purpose:

Contains the final generated MySQL query.



Rules:

- Must contain exactly one SQL statement.
- Must contain only SELECT query.
- Must be executable MySQL syntax.
- Must not contain markdown formatting.
- Must not contain comments.
- Must not contain multiple statements.



Example:


"SELECT c.contact_name, SUM(o.total_amount) AS total_sales FROM customers c JOIN orders o ON c.id=o.customer_id GROUP BY c.contact_name ORDER BY total_sales DESC LIMIT 10"



Invalid examples:


```sql
SELECT *
FROM customers;