import json
import logging
from typing import Any


from pydantic import ValidationError


from ..schemas.ai import AIGeneratedResponse



logger = logging.getLogger(__name__)



class JSONParserError(Exception):
    """
    Base exception for JSON parser errors.
    """



class InvalidJSONError(JSONParserError):
    """
    Raised when AI response is not valid JSON.
    """



class InvalidAIResponseError(JSONParserError):
    """
    Raised when AI JSON structure is invalid.
    """




class GeminiJSONParser:
    """
    Safely parse and validate Gemini responses.

    Responsibilities:
    - Clean raw AI output
    - Parse JSON
    - Validate structure
    - Normalize response

    Does NOT:
    - Execute SQL
    - Validate SQL
    - Access database
    """



    def parse(
        self,
        raw_response: str,
    ) -> AIGeneratedResponse:
        """
        Convert raw Gemini response into
        trusted internal object.
        """


        logger.info(
            "Parsing Gemini response"
        )


        cleaned_response = (
            self._clean_response(
                raw_response
            )
        )


        json_data = (
            self._decode_json(
                cleaned_response
            )
        )


        return (
            self._validate_response(
                json_data
            )
        )



    def _clean_response(
        self,
        response: str,
    ) -> str:
        """
        Remove markdown formatting.
        """


        cleaned = response.strip()


        if cleaned.startswith(
            "```"
        ):

            cleaned = (
                cleaned
                .replace(
                    "```json",
                    "",
                )
                .replace(
                    "```",
                    "",
                )
                .strip()
            )


        return cleaned



    def _decode_json(
        self,
        response: str,
    ) -> dict[str, Any]:
        """
        Decode JSON safely.
        """


        try:

            data = json.loads(
                response
            )


        except json.JSONDecodeError as error:

            logger.error(
                "Invalid JSON response: %s",
                error,
            )

            raise InvalidJSONError(
                "Gemini response is not valid JSON"
            )


        if not isinstance(
            data,
            dict,
        ):

            raise InvalidJSONError(
                "Gemini JSON response must be object"
            )


        return data



    def _validate_response(
        self,
        data: dict[str, Any],
    ) -> AIGeneratedResponse:
        """
        Validate AI response schema.
        """


        required_fields = [

            "sql",

            "summary",

            "confidence",

            "tables_used",

            "read_only",

        ]


        missing_fields = [

            field

            for field in required_fields

            if field not in data

        ]


        if missing_fields:

            raise InvalidAIResponseError(
                f"Missing fields: {missing_fields}"
            )


        try:

            validated = AIGeneratedResponse(
                **data
            )


        except ValidationError as error:

            logger.error(
                "AI response validation failed: %s",
                error,
            )


            raise InvalidAIResponseError(
                "Invalid AI response structure"
            )


        return validated




json_parser = GeminiJSONParser()