from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.orm import Session

from ...auth.jwt_handler import get_current_user

from ...database import get_app_db

from ...models.user import User

from ...schemas.connection import (
    ConnectionCreate,
    ConnectionResponse,
)

from ...services.connection_service import (
    DuplicateConnectionError,
    connection_service,
)



router = APIRouter(
    prefix="/api/connections",
    tags=["Database Connections"],
)





@router.post("/test")
def test_connection(
    connection_data: ConnectionCreate,
    current_user: User = Depends(get_current_user),
):

    result = connection_service.test_connection(
        host=connection_data.host,
        port=connection_data.port,
        database_name=connection_data.database_name,
        username=connection_data.username,
        password=connection_data.password,
    )


    if not result["success"]:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["message"],
        )


    return result





@router.post(
    "",
    response_model=ConnectionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_connection(
    connection_data: ConnectionCreate,
    database: Session = Depends(get_app_db),
    current_user: User = Depends(get_current_user),
):

    try:

        connection = (
            connection_service.create_connection(
                database=database,
                user_id=current_user.id,
                connection_data=connection_data,
            )
        )

    except DuplicateConnectionError as exc:

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Connection with this name already exists",
        ) from exc


    return connection





@router.get(
    "",
    response_model=list[ConnectionResponse],
)
def get_connections(
    database: Session = Depends(get_app_db),
    current_user: User = Depends(get_current_user),
):

    return (
        connection_service.get_user_connections(
            database=database,
            user_id=current_user.id,
        )
    )





@router.put(
    "/{connection_id}",
    response_model=ConnectionResponse,
)
def update_connection(
    connection_id: int,
    connection_data: ConnectionCreate,
    database: Session = Depends(get_app_db),
    current_user: User = Depends(get_current_user),
):


    updated = (
        connection_service.update_connection(
            database=database,
            connection_id=connection_id,
            user_id=current_user.id,
            connection_data=connection_data,
        )
    )


    if not updated:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Connection not found",
        )


    return updated





@router.delete(
    "/{connection_id}",
)
def delete_connection(
    connection_id: int,
    database: Session = Depends(get_app_db),
    current_user: User = Depends(get_current_user),
):

    deleted = (
        connection_service.delete_connection(
            database=database,
            connection_id=connection_id,
            user_id=current_user.id,
        )
    )


    if not deleted:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Connection not found",
        )


    return {
        "message":
        "Connection deleted successfully"
    }