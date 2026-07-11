import json
import logging
import time
from typing import Any

from google import genai


from ..config import settings

from ..schemas.ai import AIGeneratedResponse

from ..utils.prompt_loader import load_prompt

from ..parsers.json_parser import json_parser



logger = logging.getLogger(__name__)




class GeminiAIService:
    """
    Handles Gemini AI communication.

    Responsibilities:
    - Create Gemini client
    - Build prompts
    - Generate responses

    Parsing responsibility is handled by:
    JSON Parser Layer
    """



    def __init__(self):

        logger.info(
            "Initializing Gemini client"
        )


        logger.info(
            "Gemini model: %s",
            settings.GEMINI_MODEL,
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


        raw_response = self._call_gemini(
            prompt
        )


        parsed_response = json_parser.parse(
            raw_response
        )


        return parsed_response




    def _build_prompt(
        self,
        schema_context: dict[str, Any],
        user_prompt: str,
    ) -> str:
        """
        Build Gemini prompt.
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
        Call Gemini API with retry.
        """


        last_error = None


        for attempt in range(
            1,
            self.max_retries + 1,
        ):

            try:

                logger.info(
                    "Gemini attempt %s",
                    attempt,
                )


                response = self.client.models.generate_content(
                    model=self.model,

                    contents=prompt,
                )


                if not response.text:

                    raise RuntimeError(
                        "Empty Gemini response"
                    )


                return response.text



            except Exception as error:


                last_error = error


                logger.warning(
                    "Gemini attempt failed: %s",
                    error,
                )


                if attempt < self.max_retries:

                    time.sleep(
                        attempt * 2
                    )



        raise RuntimeError(
            f"Gemini request failed: {last_error}"
        )




ai_service = GeminiAIService()