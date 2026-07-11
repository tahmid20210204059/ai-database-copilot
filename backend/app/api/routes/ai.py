from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy import select
from sqlalchemy.orm import Session


from ...auth.jwt_handler import get_current_user

from ...database import get_app_db

from ...models.user import User

from ...models.connection import DatabaseConnection

from ...schemas.ai import (
    AIQueryRequest,
    AIGeneratedResponse,
)

from ...services.schema_service import (
    schema_service,
)

from ...services.ai_service import (
    ai_service,
)



router = APIRouter(
    prefix="/api/ai",
    tags=["AI Generation"],
)



@router.post(
    "/generate",
    response_model=AIGeneratedResponse,
)
def generate_ai_sql(
    request: AIQueryRequest,
    database: Session = Depends(get_app_db),
    current_user: User = Depends(get_current_user),
):
    """
    Generate SQL using Gemini based on database schema.

    This endpoint only generates SQL.
    It does not execute SQL.
    """

    try:

        connection = database.scalar(
            select(DatabaseConnection)
            .where(
                DatabaseConnection.id
                ==
                request.connection_id,

                DatabaseConnection.user_id
                ==
                current_user.id,
            )
        )


        if connection is None:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Database connection not found",
            )



        schema = schema_service.extract_schema(
            host=connection.host,

            port=connection.port,

            database_name=connection.database_name,

            username=connection.username,

            encrypted_password=
                connection.encrypted_password,
        )



        result = ai_service.generate_sql(
            schema_context=schema,

            user_prompt=request.prompt,
        )


        return result



    except HTTPException:

        raise



    except Exception as error:


        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,

            detail=f"AI generation failed: {str(error)}",
        )