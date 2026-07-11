import json
import logging
import time
from typing import Any

from google import genai

from ..config import settings
from ..schemas.ai import AIGeneratedResponse
from ..utils.prompt_loader import load_prompt


logger = logging.getLogger(__name__)


class GeminiAIService:
    """
    Handles Gemini AI communication.

    Responsibilities:
    - Create Gemini client
    - Build prompts
    - Generate responses
    - Retry temporary failures
    - Validate AI output
    """


    def __init__(self):

        logger.info(
            "Initializing Gemini client"
        )

        logger.info(
            "Gemini model: %s",
            settings.GEMINI_MODEL,
        )

        logger.info(
            "Gemini key prefix: %s",
            settings.GEMINI_API_KEY[:10],
        )


        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )


        self.model = settings.GEMINI_MODEL

        self.max_retries = 3



    def generate_sql(
        self,
        schema_context: dict[str, Any],
        user_prompt: str,
    ) -> AIGeneratedResponse:
        """
        Generate SQL from natural language request.
        """


        prompt = self._build_prompt(
            schema_context,
            user_prompt,
        )


        response_text = self._call_gemini(
            prompt
        )


        parsed_response = self._parse_response(
            response_text
        )


        return AIGeneratedResponse(
            **parsed_response
        )



    def _build_prompt(
        self,
        schema_context: dict[str, Any],
        user_prompt: str,
    ) -> str:
        """
        Build final Gemini prompt.
        """


        template = load_prompt(
            "generate_sql.txt"
        )


        return template.format(
            schema_context=json.dumps(
                schema_context,
                indent=2,
            ),

            user_prompt=user_prompt,
        )



    def _call_gemini(
        self,
        prompt: str,
    ) -> str:
        """
        Call Gemini API with retry support.

        Temporary simplified configuration
        for API validation.
        """


        last_error = None


        for attempt in range(
            1,
            self.max_retries + 1,
        ):

            try:

                logger.info(
                    "Gemini request attempt %s",
                    attempt,
                )


                response = self.client.models.generate_content(
                    model=self.model,

                    contents=prompt,
                )


                if not response.text:

                    raise RuntimeError(
                        "Gemini returned empty response"
                    )


                logger.info(
                    "Gemini response received successfully"
                )


                return response.text



            except Exception as error:

                last_error = error


                logger.warning(
                    "Gemini attempt %s failed: %s",
                    attempt,
                    error,
                )


                if attempt < self.max_retries:

                    time.sleep(
                        attempt * 2
                    )



        raise RuntimeError(
            f"Gemini request failed: {last_error}"
        )



    def _parse_response(
        self,
        response_text: str,
    ) -> dict:
        """
        Parse Gemini JSON response.
        """


        cleaned = response_text.strip()


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


        try:

            data = json.loads(
                cleaned
            )


        except json.JSONDecodeError as error:

            raise RuntimeError(
                f"Invalid Gemini JSON response: {error}"
            )



        required_fields = [
            "sql",
            "summary",
            "confidence",
            "tables_used",
            "read_only",
        ]


        for field in required_fields:

            if field not in data:

                raise RuntimeError(
                    f"Missing AI response field: {field}"
                )


        return data



ai_service = GeminiAIService()