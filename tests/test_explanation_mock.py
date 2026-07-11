from unittest.mock import patch

from backend.app.services.explanation_service import (
    explanation_service,
)



def test_explanation_mock_success():

    fake_response = type(
        "Response",
        (),
        {
            "text":
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
        }
    )


    with patch.object(

        explanation_service.client.models,

        "generate_content",

        return_value=fake_response,

    ):


        result = explanation_service.explain(

            sql=
            "SELECT * FROM customers"

        )


        assert result.explanation

        assert len(
            result.key_points
        ) == 2



def test_explanation_mock_invalid():

    fake_response = type(
        "Response",
        (),
        {
            "text":
            "invalid json"
        }
    )


    with patch.object(

        explanation_service.client.models,

        "generate_content",

        return_value=fake_response,

    ):


        try:

            explanation_service.explain(
                sql="SELECT 1"
            )


            assert False


        except Exception:

            assert True