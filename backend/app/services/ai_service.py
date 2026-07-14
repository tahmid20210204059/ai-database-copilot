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
    Handles enterprise Gemini AI communication.

    Responsibilities:

    - Load modular AI prompt architecture
    - Build production-grade prompts
    - Provide schema context
    - Generate SQL responses
    - Handle Gemini communication
    - Parse structured JSON output


    Prompt Architecture:

    system_prompt.md
        +
    business_rules.md
        +
    sql_generation_rules.md
        +
    output_contract.md
        +
    domain examples
        +
    schema context
        +
    user request

        ↓

    Gemini

        ↓

    JSON SQL Response
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
        Build modular enterprise prompt.
        """



        system_prompt = load_prompt(

            "system_prompt.md"

        )



        business_rules = load_prompt(

            "business_rules.md"

        )



        sql_rules = load_prompt(

            "sql_generation_rules.md"

        )



        output_contract = load_prompt(

            "output_contract.md"

        )



        examples = self._load_examples()






        return f"""

{system_prompt}



==================================================
BUSINESS RULES
==================================================

{business_rules}



==================================================
SQL GENERATION RULES
==================================================

{sql_rules}



==================================================
OUTPUT CONTRACT
==================================================

{output_contract}



==================================================
FEW SHOT EXAMPLES
==================================================

{examples}



==================================================
DATABASE SCHEMA
==================================================

{json.dumps(
    schema_context,
    indent=2,
)}



==================================================
USER REQUEST
==================================================

{user_prompt}

"""








    def _load_examples(self) -> str:
        """
        Load domain examples.

        These examples improve business intent understanding.
        """



        example_files = [

            "examples/crm_examples.md",

            "examples/sales_examples.md",

            "examples/inventory_examples.md",

            "examples/finance_examples.md",

        ]



        examples = []



        for file in example_files:


            try:


                examples.append(

                    load_prompt(
                        file
                    )

                )


            except Exception as error:


                logger.warning(

                    "Example loading failed: %s",

                    error,

                )



        return "\n\n".join(
            examples
        )









    def _call_gemini(
        self,
        prompt: str,
    ) -> str:
        """
        Call Gemini API with retry mechanism.
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





                response = (

                    self.client.models.generate_content(

                        model=self.model,

                        contents=prompt,

                    )

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