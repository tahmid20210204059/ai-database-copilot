import requests


BASE_URL = "http://127.0.0.1:8000"


email = "test20260711130712@example.com"
password = "StrongPass123!"


def test_connection_save_flow():
    print("========== LOGIN TEST ==========")

    login_response = requests.post(
        f"{BASE_URL}/api/login",
        json={
            "email": email,
            "password": password,
        },
    )

    print("Login Status:", login_response.status_code)
    assert login_response.status_code == 200

    login_data = login_response.json()
    token = login_data["access_token"]

    print("JWT received:", bool(token))

    headers = {
        "Authorization": f"Bearer {token}"
    }

    print("\n========== CONNECTION TEST ==========")

    connection_data = {
        "connection_name": "Enterprise Sales Database",
        "host": "localhost",
        "port": 3306,
        "database_name": "enterprise_sales",
        "username": "copilot_reader",
        "password": "ReaderLocal_2026_R8m4",
        "ssl_enabled": False,
    }

    test_response = requests.post(
        f"{BASE_URL}/api/connections/test",
        json=connection_data,
        headers=headers,
    )

    print("Connection Test Status:", test_response.status_code)
    assert test_response.status_code == 200
    print(test_response.json())

    print("\n========== SAVE CONNECTION ==========")

    save_response = requests.post(
        f"{BASE_URL}/api/connections",
        json=connection_data,
        headers=headers,
    )

    print("Save Status:", save_response.status_code)
    print(save_response.text)

    assert save_response.status_code == 409
    assert save_response.json() == {"detail": "Connection with this name already exists"}