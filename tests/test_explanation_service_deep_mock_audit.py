from unittest.mock import patch

import pytest


from backend.app.services.explanation_service import (
    explanation_service,
)

from backend.app.utils.ai_exceptions import (
    AIRateLimitError,
    AITimeoutError,
)



def section(title):

    print("\n" + "=" * 70)

    print(title)

    print("=" * 70)



class FakeResponse:

    def __init__(
        self,
        text,
    ):
        self.text = text




def test_valid_json_response():

    section(
        "1. VALID JSON RESPONSE TEST"
    )


    fake = FakeResponse(
        """
        {
            "explanation":
            "This query reads customer data",

            "key_points":
            [
                "Uses SELECT",
                "Reads customers table"
            ],

            "complexity":
            "Simple"
        }
        """
    )


    with patch.object(
        explanation_service.client.models,
        "generate_content",
        return_value=fake,
    ):

        result = explanation_service.explain(
            sql="SELECT * FROM customers"
        )


    print(result)


    assert result.explanation

    assert len(result.key_points) == 2



def test_markdown_json_response():

    section(
        "2. MARKDOWN JSON TEST"
    )


    fake = FakeResponse(
        """
        ```json
        {
            "explanation":"Reads data",
            "key_points":[
                "SELECT operation"
            ],
            "complexity":"Easy"
        }
        ```
        """
    )


    with patch.object(
        explanation_service.client.models,
        "generate_content",
        return_value=fake,
    ):

        result = explanation_service.explain(
            sql="SELECT 1"
        )


    print(result)


    assert result.complexity == "Easy"



def test_object_key_points_normalization():

    section(
        "3. KEY POINT NORMALIZATION TEST"
    )


    fake = FakeResponse(
        """
        {
            "explanation":
            "Join explanation",

            "key_points":
            [
                {
                    "clause":"JOIN",
                    "description":
                    "Combines tables"
                }
            ],

            "complexity":
            "Medium"
        }
        """
    )


    with patch.object(
        explanation_service.client.models,
        "generate_content",
        return_value=fake,
    ):

        result = explanation_service.explain(
            sql="SELECT * FROM a JOIN b"
        )


    print(result)


    assert result.key_points[0] == (
        "JOIN: Combines tables"
    )



def test_missing_optional_fields():

    section(
        "4. MISSING FIELD NORMALIZATION"
    )


    fake = FakeResponse(
        """
        {
            "explanation":
            "Simple explanation"
        }
        """
    )


    with patch.object(
        explanation_service.client.models,
        "generate_content",
        return_value=fake,
    ):

        result = explanation_service.explain(
            sql="SELECT 1"
        )


    print(result)


    assert result.explanation

    assert result.key_points == []

    assert result.complexity == "Unknown"



def test_invalid_json():

    section(
        "5. INVALID JSON TEST"
    )


    fake = FakeResponse(
        "invalid json"
    )


    with patch.object(
        explanation_service.client.models,
        "generate_content",
        return_value=fake,
    ):


        with pytest.raises(
            RuntimeError
        ):

            explanation_service.explain(
                sql="SELECT 1"
            )



def test_rate_limit_handling():

    section(
        "6. RATE LIMIT TEST"
    )


    with patch.object(

        explanation_service.client.models,

        "generate_content",

        side_effect=Exception(
            "429 RESOURCE_EXHAUSTED quota exceeded"
        ),

    ):


        with pytest.raises(
            AIRateLimitError
        ):

            explanation_service.explain(
                sql="SELECT 1"
            )



def test_timeout_handling():

    section(
        "7. TIMEOUT TEST"
    )


    with patch.object(

        explanation_service.client.models,

        "generate_content",

        side_effect=Exception(
            "request timeout"
        ),

    ):


        with pytest.raises(
            AITimeoutError
        ):

            explanation_service.explain(
                sql="SELECT 1"
            )



def test_final():

    section(
        "FINAL RESULT"
    )


    print(
        "EXPLANATION SERVICE MOCK AUDIT PASSED"
    )