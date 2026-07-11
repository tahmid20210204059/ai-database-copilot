import json
import logging
import time
from typing import Any


from google import genai


from ..config import settings

from ..schemas.explanation import (
    SQLExplanationResponse,
)

from ..utils.prompt_loader import load_prompt

from ..parsers.json_parser import (
    InvalidJSONError,
    InvalidAIResponseError,
)

from ..utils.ai_exceptions import (
    AIRateLimitError,
    AITimeoutError,
)



logger = logging.getLogger(__name__)




class SQLExplanationService:
    """
    Generates human-readable SQL explanations.

    Responsibilities:
    - Build explanation prompt
    - Call Gemini
    - Handle AI failures
    - Parse AI response
    - Normalize AI output
    - Validate explanation structure

    Does NOT:
    - Execute SQL
    - Validate SQL
    - Modify SQL
    """



    def __init__(self):

        logger.info(
            "Initializing SQL explanation service"
        )


        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )


        self.model = settings.GEMINI_MODEL


        self.max_retries = 2




    def explain(
        self,
        sql: str,
        context: str | None = None,
    ) -> SQLExplanationResponse:
        """
        Generate explanation for SQL query.
        """


        if not sql or not sql.strip():

            raise ValueError(
                "SQL query cannot be empty"
            )



        prompt_template = load_prompt(
            "explain_sql.txt"
        )


        final_prompt = prompt_template.format(

            sql=sql,

            context=context or "No context provided",

        )



        try:

            logger.info(
                "Requesting SQL explanation from Gemini"
            )


            response = self._call_gemini(
                final_prompt
            )



            if not response.text:

                raise RuntimeError(
                    "Empty Gemini explanation response"
                )



            parsed_response = self._parse_response(
                response.text
            )



            return SQLExplanationResponse(
                **parsed_response
            )



        except (
            InvalidJSONError,
            InvalidAIResponseError,
        ) as error:


            logger.error(
                "Explanation parsing failed: %s",
                error,
            )


            raise RuntimeError(
                "Invalid AI explanation response"
            )



        except (
            AIRateLimitError,
            AITimeoutError,
        ):

            raise



        except Exception as error:


            logger.error(
                "SQL explanation failed: %s",
                error,
            )


            raise RuntimeError(
                "Failed to generate SQL explanation"
            )





    def _call_gemini(
        self,
        prompt: str,
    ):
        """
        Call Gemini API with retry and error handling.
        """


        last_error = None



        for attempt in range(
            1,
            self.max_retries + 1,
        ):

            try:

                logger.info(
                    "Gemini explanation attempt %s",
                    attempt,
                )



                return self.client.models.generate_content(

                    model=self.model,

                    contents=prompt,

                )



            except Exception as error:


                last_error = error


                error_text = str(error).lower()



                logger.warning(
                    "Gemini attempt %s failed: %s",
                    attempt,
                    error,
                )



                if (
                    "429" in error_text
                    or
                    "quota" in error_text
                    or
                    "resource_exhausted" in error_text
                ):


                    raise AIRateLimitError(
                        "Gemini quota exceeded. Please try again later."
                    )



                if (
                    "timeout" in error_text
                    or
                    "timed out" in error_text
                ):


                    if attempt < self.max_retries:

                        time.sleep(
                            attempt * 2
                        )

                        continue



                    raise AITimeoutError(
                        "Gemini request timeout"
                    )



                raise



        raise RuntimeError(
            f"Gemini failed: {last_error}"
        )





    def _parse_response(
        self,
        raw_response: str,
    ) -> dict[str, Any]:
        """
        Parse and normalize Gemini JSON response.
        """



        cleaned = self._clean_json_response(
            raw_response
        )



        try:

            data = json.loads(
                cleaned
            )



        except json.JSONDecodeError as error:


            logger.error(
                "Invalid explanation JSON: %s",
                error,
            )


            raise InvalidJSONError(
                "Gemini explanation is not valid JSON"
            )



        if not isinstance(
            data,
            dict,
        ):

            raise InvalidAIResponseError(
                "AI response must be a JSON object"
            )



        return self._normalize_response(
            data
        )





    def _clean_json_response(
        self,
        response: str,
    ) -> str:
        """
        Remove markdown wrappers from Gemini response.
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





    def _normalize_response(
        self,
        data: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Normalize different Gemini output formats.
        """



        explanation = data.get(
            "explanation"
        )


        if not explanation:

            explanation = (
                "No explanation was generated."
            )



        key_points = data.get(
            "key_points",
            []
        )



        if not isinstance(
            key_points,
            list,
        ):

            key_points = []



        normalized_points = []



        for item in key_points:


            if isinstance(
                item,
                str,
            ):

                normalized_points.append(
                    item
                )



            elif isinstance(
                item,
                dict,
            ):


                clause = item.get(
                    "clause",
                    ""
                )


                description = item.get(
                    "description",
                    ""
                )



                if clause and description:

                    normalized_points.append(
                        f"{clause}: {description}"
                    )


                elif description:

                    normalized_points.append(
                        description
                    )



        complexity = data.get(
            "complexity"
        )


        if not complexity:

            complexity = "Unknown"



        return {

            "explanation":
            explanation,


            "key_points":
            normalized_points,


            "complexity":
            complexity,

        }





explanation_service = SQLExplanationService()