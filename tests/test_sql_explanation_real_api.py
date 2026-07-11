import json

import pytest

pytestmark = pytest.mark.real_api

from backend.app.services.explanation_service import (
    explanation_service,
)

from backend.app.schemas.explanation import (
    SQLExplanationResponse,
)


def section(title):

    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)



def validate_response(result):

    assert isinstance(
        result,
        SQLExplanationResponse
    )

    assert result.explanation

    assert isinstance(
        result.key_points,
        list
    )

    assert result.complexity



def test_simple_select_explanation():

    section(
        "1. SIMPLE SELECT EXPLANATION"
    )


    sql = """
    SELECT *
    FROM customers
    LIMIT 5
    """


    result = explanation_service.explain(
        sql=sql,
        context="customers table contains customer information",
    )


    print(result)


    validate_response(result)



def test_join_query_explanation():

    section(
        "2. JOIN QUERY EXPLANATION"
    )


    sql = """
    SELECT
        c.company_name,
        so.total_amount
    FROM customers c
    JOIN sales_orders so
    ON c.id = so.customer_id
    LIMIT 5
    """


    result = explanation_service.explain(
        sql=sql,
        context="""
        customers stores customer details.
        sales_orders stores order information.
        """,
    )


    print(result)


    validate_response(result)



def test_aggregation_query_explanation():

    section(
        "3. AGGREGATION QUERY EXPLANATION"
    )


    sql = """
    SELECT
        customer_id,
        SUM(total_amount)
    FROM sales_orders
    GROUP BY customer_id
    """


    result = explanation_service.explain(
        sql=sql,
        context="sales_orders contains transaction data",
    )


    print(result)


    validate_response(result)



def test_no_sql_modification():

    section(
        "4. SQL MODIFICATION CHECK"
    )


    sql = """
    SELECT *
    FROM customers
    """


    result = explanation_service.explain(
        sql=sql
    )


    print(result)


    text = result.explanation.lower()


    assert "update" not in text

    assert "delete" not in text



def test_security_leakage():

    section(
        "5. SECURITY CHECK"
    )


    sql = """
    SELECT *
    FROM customers
    """


    result = explanation_service.explain(
        sql=sql
    )


    response_text = result.model_dump_json().lower()


    assert "password" not in response_text

    assert "api_key" not in response_text

    assert "secret" not in response_text



def test_final():

    section(
        "FINAL RESULT"
    )


    print(
        "SQL EXPLANATION DEEP AUDIT PASSED"
    )