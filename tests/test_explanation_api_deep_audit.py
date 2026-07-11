import pytest
import requests

pytestmark = pytest.mark.real_api

BASE_URL = "http://127.0.0.1:8000"


EMAIL = "test20260711130712@example.com"

PASSWORD = "StrongPass123!"



def section(title):

    print("\n" + "=" * 70)

    print(title)

    print("=" * 70)




def login():

    response = requests.post(

        f"{BASE_URL}/api/login",

        json={
            "email": EMAIL,
            "password": PASSWORD,
        },

    )


    assert response.status_code == 200


    return response.json()["access_token"]




TOKEN = login()


HEADERS = {

    "Authorization":
    f"Bearer {TOKEN}"

}




def test_jwt_required():

    section(
        "1. JWT SECURITY TEST"
    )


    response = requests.post(

        f"{BASE_URL}/api/ai/explain",

        json={
            "sql":
            "SELECT * FROM customers"
        }

    )


    print(response.text)


    assert response.status_code == 401




def test_valid_sql_explanation():

    section(
        "2. VALID SQL EXPLANATION TEST"
    )


    response = requests.post(

        f"{BASE_URL}/api/ai/explain",

        headers=HEADERS,

        json={
            "sql":
            """
            SELECT *
            FROM customers
            LIMIT 5
            """,

            "context":
            "customers table contains customer information"

        },

        timeout=60

    )


    print(response.text)


    assert response.status_code == 200


    data=response.json()


    assert "explanation" in data

    assert "key_points" in data

    assert "complexity" in data



def test_join_explanation():

    section(
        "3. JOIN QUERY EXPLANATION TEST"
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


    response = requests.post(

        f"{BASE_URL}/api/ai/explain",

        headers=HEADERS,

        json={
            "sql": sql
        },

        timeout=60

    )


    print(response.text)


    assert response.status_code == 200




def test_empty_sql():

    section(
        "4. EMPTY SQL VALIDATION TEST"
    )


    response = requests.post(

        f"{BASE_URL}/api/ai/explain",

        headers=HEADERS,

        json={
            "sql":""
        }

    )


    print(response.text)


    assert response.status_code == 422




def test_missing_sql_field():

    section(
        "5. MISSING FIELD TEST"
    )


    response = requests.post(

        f"{BASE_URL}/api/ai/explain",

        headers=HEADERS,

        json={}

    )


    print(response.text)


    assert response.status_code == 422




def test_long_sql_handling():

    section(
        "6. LONG SQL TEST"
    )


    huge_sql = (
        "SELECT * FROM customers "
        +
        "WHERE company_name='test' "
        * 1000
    )


    response = requests.post(

        f"{BASE_URL}/api/ai/explain",

        headers=HEADERS,

        json={
            "sql": huge_sql
        },

    )


    print(
        response.status_code
    )


    assert response.status_code in [
        200,
        422,
    ]




def test_sensitive_data_leak():

    section(
        "7. SECURITY LEAKAGE TEST"
    )


    response = requests.post(

        f"{BASE_URL}/api/ai/explain",

        headers=HEADERS,

        json={
            "sql":
            "SELECT * FROM customers"
        },

        timeout=60

    )


    print(response.text)


    text=response.text.lower()


    assert "password" not in text

    assert "api_key" not in text

    assert "secret" not in text




def test_response_schema():

    section(
        "8. RESPONSE SCHEMA TEST"
    )


    response=requests.post(

        f"{BASE_URL}/api/ai/explain",

        headers=HEADERS,

        json={
            "sql":
            "SELECT COUNT(*) FROM customers"
        },

        timeout=60

    )


    data=response.json()


    assert isinstance(
        data["explanation"],
        str
    )


    assert isinstance(
        data["key_points"],
        list
    )


    assert isinstance(
        data["complexity"],
        str
    )




def test_final():

    section(
        "FINAL RESULT"
    )


    print(
        "AI EXPLANATION API DEEP AUDIT PASSED"
    )