from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy import (
    select,
    func,
)

from sqlalchemy.orm import Session


from ...auth.permissions import require_user

from ...database import get_app_db

from ...models.user import User

from ...models.connection import DatabaseConnection

from ...models.query_history import QueryHistory



router = APIRouter(
    prefix="/api/user",
    tags=["User Dashboard"],
)





@router.get("/stats")
def get_user_stats(
    database: Session = Depends(get_app_db),
    current_user: User = Depends(require_user),
):
    """
    Return current user's dashboard statistics.
    """


    total_connections = database.scalar(
        select(
            func.count(
                DatabaseConnection.id
            )
        )
        .where(
            DatabaseConnection.user_id
            ==
            current_user.id
        )
    )



    total_queries = database.scalar(
        select(
            func.count(
                QueryHistory.id
            )
        )
        .where(
            QueryHistory.user_id
            ==
            current_user.id
        )
    )



    successful_queries = database.scalar(
        select(
            func.count(
                QueryHistory.id
            )
        )
        .where(
            QueryHistory.user_id
            ==
            current_user.id,
            
            QueryHistory.status
            ==
            "success"
        )
    )



    success_rate = 0


    if total_queries:

        success_rate = round(
            (
                successful_queries
                /
                total_queries
            )
            * 100,
            2,
        )



    return {

        "total_connections":
        total_connections or 0,


        "total_queries":
        total_queries or 0,


        "success_rate":
        success_rate,


    }