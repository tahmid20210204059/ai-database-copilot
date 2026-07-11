import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(
    0,
    str(PROJECT_ROOT)
)


import json
import requests


from backend.app.config import settings

from backend.app.utils.prompt_loader import load_prompt

from backend.app.services.ai_service import ai_service

from backend.app.schemas.ai import (
    AIQueryRequest,
    AIGeneratedResponse,
)



BASE_URL = "http://127.0.0.1:8000"


EMAIL = "test20260711130712@example.com"

PASSWORD = "StrongPass123!"



def section(name):

    print("\n" + "=" * 70)

    print(name)

    print("=" * 70)



def test_config():

    section(
        "1. GEMINI CONFIGURATION"
    )


    print(
        "API Key Exists:",
        bool(settings.GEMINI_API_KEY)
    )

    print(
        "API Key Length:",
        len(settings.GEMINI_API_KEY)
    )


    print(
        "Model:",
        settings.GEMINI_MODEL
    )


    print(
        "Temperature:",
        settings.GEMINI_TEMPERATURE
    )


    assert settings.GEMINI_API_KEY

    print(
        "CONFIGURATION PASS"
    )



def test_sdk():

    section(
        "2. GEMINI SDK CLIENT"
    )


    print(
        "Client:",
        ai_service.client
    )


    print(
        "Model:",
        ai_service.model
    )


    assert ai_service.client

    print(
        "SDK CLIENT PASS"
    )



def test_prompt():

    section(
        "3. PROMPT MANAGEMENT"
    )


    prompt = load_prompt(
        "generate_sql.txt"
    )


    print(
        "Prompt length:",
        len(prompt)
    )


    assert "{schema_context}" in prompt

    assert "{user_prompt}" in prompt


    print(
        "PROMPT SYSTEM PASS"
    )



def test_schema():

    section(
        "4. AI SCHEMA VALIDATION"
    )


    request = AIQueryRequest(
        prompt="show customers",
        connection_id=1,
    )


    print(
        request
    )


    response = AIGeneratedResponse(
        sql="SELECT 1",
        summary="test",
        confidence=1.0,
        tables_used=["customers"],
        read_only=True,
    )


    print(
        response
    )


    print(
        "SCHEMA VALIDATION PASS"
    )



def login():

    response = requests.post(

        f"{BASE_URL}/api/login",

        json={
            "email":EMAIL,
            "password":PASSWORD,
        }

    )


    assert response.status_code == 200


    return response.json()["access_token"]



def test_api():

    section(
        "5. AI API ENDPOINT"
    )


    token = login()


    response = requests.post(

        f"{BASE_URL}/api/ai/generate",

        headers={
            "Authorization":
            f"Bearer {token}"
        },

        json={
            "connection_id":1,

            "prompt":
            "Show top 5 customers by revenue"
        },

        timeout=60

    )


    print(
        "Status:",
        response.status_code
    )


    print(
        response.text[:500]
    )


    assert response.status_code == 200


    data = response.json()


    assert "sql" in data

    assert "summary" in data

    assert "confidence" in data


    print(
        "API GENERATION PASS"
    )



def main():

    test_config()

    test_sdk()

    test_prompt()

    test_schema()

    test_api()


    section(
        "FINAL RESULT"
    )


    print(
        "GEMINI INTEGRATION FULL AUDIT PASSED"
    )



if __name__ == "__main__":

    main()