import logging


from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from fastapi.responses import JSONResponse


from pydantic import BaseModel, Field


from ...auth.permissions import require_user

from ...models.user import User


from ...schemas.explanation import (
    SQLExplanationResponse,
)


from ...services.explanation_service import (
    explanation_service,
)


from ...utils.ai_exceptions import (
    AIRateLimitError,
    AITimeoutError,
)





logger = logging.getLogger(__name__)





router = APIRouter(

    prefix="/api/ai",

    tags=[
        "AI Explanation"
    ],

)








class SQLExplanationAPIRequest(BaseModel):
    """
    API request schema for SQL explanation.
    """


    sql: str = Field(

        ...,

        min_length=1,

        max_length=10000,

        description="SQL query to explain",

    )


    context: str | None = Field(

        default=None,

        max_length=5000,

        description="Optional database context",

    )









@router.post(
    "/explain",
    response_model=SQLExplanationResponse,
)
def explain_sql(

    request: SQLExplanationAPIRequest,

    current_user: User = Depends(
        require_user
    ),

):
    """
    Generate human-readable SQL explanation.

    Only normal users can use AI explanation.

    This endpoint:

    - Does not execute SQL
    - Does not validate SQL
    - Only explains SQL
    """



    try:


        logger.info(

            "SQL explanation requested by user_id=%s",

            current_user.id,

        )



        result = explanation_service.explain(

            sql=request.sql,

            context=request.context,

        )



        return result






    except ValueError as error:


        raise HTTPException(

            status_code=status.HTTP_400_BAD_REQUEST,

            detail=str(error),

        )







    except AIRateLimitError as error:


        logger.warning(

            "Gemini rate limit reached for user_id=%s",

            current_user.id,

        )



        return JSONResponse(

            status_code=429,

            content={

                "error_code":
                "AI_RATE_LIMIT",


                "message":
                "AI service temporarily unavailable",


                "retry_after_seconds":
                error.retry_after_seconds,

            },

        )









    except AITimeoutError as error:


        logger.warning(

            "Gemini timeout for user_id=%s",

            current_user.id,

        )



        return JSONResponse(

            status_code=504,

            content={

                "error_code":
                "AI_TIMEOUT",


                "message":
                "AI request timed out",

            },

        )









    except Exception as error:


        logger.error(

            "Explanation API failed: %s",

            error,

        )



        raise HTTPException(

            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,

            detail="Failed to generate SQL explanation",

        )