import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(
    0,
    str(PROJECT_ROOT)
)

import requests

from sqlalchemy import text

from backend.app.database import app_engine


BASE_URL = "http://127.0.0.1:8000"


TEST_EMAIL = "test20260711130712@example.com"
TEST_PASSWORD = "StrongPass123!"


def login():

    response = requests.post(
        f"{BASE_URL}/api/login",
        json={
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD,
        },
    )

    assert response.status_code == 200

    data = response.json()

    return data["access_token"]



def test_connection_crud():

    print("\n========== LOGIN ==========")

    token = login()

    print("JWT received")


    headers = {
        "Authorization": f"Bearer {token}"
    }


    print("\n========== CREATE CONNECTION ==========")

    payload = {

        "connection_name":
            "Automated Test Sales DB",

        "host":
            "localhost",

        "port":
            3306,

        "database_name":
            "enterprise_sales",

        "username":
            "copilot_reader",

        "password":
            "ReaderLocal_2026_R8m4",

        "ssl_enabled":
            False,
    }


    create_response = requests.post(
        f"{BASE_URL}/api/connections",
        json=payload,
        headers=headers,
    )


    assert create_response.status_code == 201


    created = create_response.json()

    connection_id = created["id"]


    print(
        "Created connection ID:",
        connection_id
    )


    print("\n========== DATABASE ENCRYPTION CHECK ==========")


    with app_engine.connect() as connection:

        row = connection.execute(
            text(
                """
                SELECT encrypted_password
                FROM db_connections
                WHERE id=:id
                """
            ),
            {
                "id": connection_id
            },
        ).fetchone()


    encrypted_password = row[0]


    assert encrypted_password.startswith(
        "gAAAA"
    )


    print(
        "Password encrypted successfully"
    )


    print("\n========== GET CONNECTION ==========")


    get_response = requests.get(
        f"{BASE_URL}/api/connections",
        headers=headers,
    )


    assert get_response.status_code == 200


    connections = get_response.json()


    found = False


    for item in connections:

        if item["id"] == connection_id:
            found = True


    assert found is True


    print(
        "Connection retrieved successfully"
    )


    print("\n========== DELETE CONNECTION ==========")


    delete_response = requests.delete(
        f"{BASE_URL}/api/connections/{connection_id}",
        headers=headers,
    )


    assert delete_response.status_code == 200


    print(
        "Connection deleted successfully"
    )


    print(
        "\n========== TEST COMPLETED =========="
    )



if __name__ == "__main__":

    test_connection_crud()