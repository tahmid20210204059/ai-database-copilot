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
from ...models.connection import DatabaseConnection
from ...models.user import User
from ...schemas.schema import SchemaResponse
from ...services.schema_service import schema_service



router = APIRouter(
    prefix="/api/connections",
    tags=["Schema Extraction"],
)



@router.get(
    "/{connection_id}/schema",
    response_model=SchemaResponse,
)
def extract_database_schema(
    connection_id: int,
    database: Session = Depends(get_app_db),
    current_user: User = Depends(get_current_user),
):
    """
    Extract database metadata for owned connection.
    """


    connection = database.scalar(
        select(DatabaseConnection)
        .where(
            DatabaseConnection.id == connection_id,
            DatabaseConnection.user_id == current_user.id,
        )
    )


    if connection is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Database connection not found",
        )


    try:

        schema = schema_service.extract_schema(
            host=connection.host,
            port=connection.port,
            database_name=connection.database_name,
            username=connection.username,
            encrypted_password=connection.encrypted_password,
        )


        return schema


    except Exception as error:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
        )