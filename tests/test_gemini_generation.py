import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(
    0,
    str(PROJECT_ROOT)
)


import requests

pytestmark = pytest.mark.real_api

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




def test_gemini_generation():

    print("\n========== LOGIN ==========")

    token = login()

    print(
        "JWT received"
    )


    headers = {
        "Authorization":
            f"Bearer {token}"
    }



    print(
        "\n========== GEMINI GENERATION =========="
    )


    payload = {

        "connection_id": 1,

        "prompt":
            "Show top 10 customers by total revenue"

    }


    response = requests.post(

        f"{BASE_URL}/api/ai/generate",

        json=payload,

        headers=headers,

        timeout=60,

    )


    print(
        "Status:",
        response.status_code
    )


    print(
        "\nResponse:"
    )

    print(
        response.text
    )


    assert response.status_code == 200


    data = response.json()


    assert "sql" in data

    assert "summary" in data

    assert "confidence" in data

    assert "tables_used" in data

    assert "read_only" in data



    assert data["read_only"] is True



    print(
        "\nGemini generation successful"
    )



if __name__ == "__main__":

    test_gemini_generation()