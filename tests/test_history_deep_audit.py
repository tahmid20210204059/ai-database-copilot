import requests


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




created_history_id = None




def test_create_history():

    global created_history_id


    section(
        "1. CREATE HISTORY TEST"
    )


    payload = {

        "connection_id": 1,

        "prompt":
        "Show top customers",

        "generated_sql":
        "SELECT * FROM customers LIMIT 5",

        "explanation":
        "Returns customer list",

        "confidence":
        0.95,

        "execution_time_ms":
        35.5,

        "rows_returned":
        5,

        "status":
        "success",

        "error_message":
        None,

    }



    response = requests.post(

        f"{BASE_URL}/api/history",

        headers=HEADERS,

        json=payload,

    )


    print(response.text)


    assert response.status_code == 201


    data = response.json()


    assert data["status"] == "success"

    assert data["prompt"] == "Show top customers"


    created_history_id = data["id"]



def test_get_history():

    section(
        "2. GET HISTORY TEST"
    )


    response = requests.get(

        f"{BASE_URL}/api/history",

        headers=HEADERS,

    )


    print(response.text)


    assert response.status_code == 200


    data = response.json()


    assert "items" in data

    assert "total" in data




def test_pagination():

    section(
        "3. PAGINATION TEST"
    )


    response = requests.get(

        f"{BASE_URL}/api/history?page=1&page_size=1",

        headers=HEADERS,

    )


    print(response.text)


    assert response.status_code == 200


    data=response.json()


    assert data["page"] == 1

    assert data["page_size"] == 1



def test_status_filter():

    section(
        "4. STATUS FILTER TEST"
    )


    response = requests.get(

        f"{BASE_URL}/api/history?status=success",

        headers=HEADERS,

    )


    print(response.text)


    assert response.status_code == 200




def test_get_single_history():

    section(
        "5. GET SINGLE HISTORY TEST"
    )


    response = requests.get(

        f"{BASE_URL}/api/history/{created_history_id}",

        headers=HEADERS,

    )


    print(response.text)


    assert response.status_code == 200



def test_invalid_history_id():

    section(
        "6. INVALID ID TEST"
    )


    response=requests.get(

        f"{BASE_URL}/api/history/99999999",

        headers=HEADERS,

    )


    print(response.text)


    assert response.status_code == 404




def test_sensitive_data_leak():

    section(
        "7. SECURITY RESPONSE TEST"
    )


    response=requests.get(

        f"{BASE_URL}/api/history",

        headers=HEADERS,

    )


    text=response.text.lower()


    assert "password" not in text

    assert "api_key" not in text

    assert "encrypted_password" not in text




def test_delete_history():

    section(
        "8. DELETE HISTORY TEST"
    )


    response=requests.delete(

        f"{BASE_URL}/api/history/{created_history_id}",

        headers=HEADERS,

    )


    print(response.text)


    assert response.status_code == 200




def test_final():

    section(
        "FINAL RESULT"
    )


    print(
        "QUERY HISTORY DEEP AUDIT PASSED"
    )