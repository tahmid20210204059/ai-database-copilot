import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(
    0,
    str(PROJECT_ROOT)
)


import requests


BASE_URL = "http://127.0.0.1:8000"


EMAIL = "test20260711130712@example.com"
PASSWORD = "StrongPass123!"


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



def test_schema_extraction():

    print("\n========== LOGIN ==========")

    token = login()

    print("JWT received")


    headers = {
        "Authorization": f"Bearer {token}"
    }


    print("\n========== SCHEMA EXTRACTION ==========")


    response = requests.get(
        f"{BASE_URL}/api/connections/1/schema",
        headers=headers,
    )


    print(
        "Status:",
        response.status_code
    )

    print("\nRAW RESPONSE:")
    print(response.text)

    data = response.json()


    print(
        "Database:",
        data.get("database")
    )


    print(
        "Tables count:",
        len(data.get("tables", {}))
    )


    print(
        "Relationships count:",
        len(data.get("relationships", []))
    )
    print("\nFULL RESPONSE:")
    print(data)


    assert response.status_code == 200

    assert "tables" in data

    assert "relationships" in data


    print(
        "\nSchema extraction successful"
    )



if __name__ == "__main__":

    test_schema_extraction()