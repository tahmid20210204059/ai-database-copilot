from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy import (
    select,
    func,
)

from sqlalchemy.orm import Session


from ...auth.permissions import (
    require_owner,
)


from ...database import (
    get_app_db,
)


from ...models.user import (
    User,
)


from ...models.connection import (
    DatabaseConnection,
)


from ...models.query_history import (
    QueryHistory,
)


from ...schemas.admin import (
    AdminUserResponse,
    AdminConnectionResponse,
    AdminStatsResponse,
)





router = APIRouter(
    prefix="/api/admin",
    tags=[
        "Admin"
    ],
)









@router.get(
    "/users",
    response_model=list[AdminUserResponse],
)
def get_all_users(
    database: Session = Depends(get_app_db),
    current_user: User = Depends(require_owner),
):
    """
    Owner can view all application users.
    """


    users = database.scalars(
        select(User)
        .order_by(
            User.created_at.desc()
        )
    ).all()



    return users











@router.get(
    "/connections",
    response_model=list[AdminConnectionResponse],
)
def get_all_connections(
    database: Session = Depends(get_app_db),
    current_user: User = Depends(require_owner),
):
    """
    Owner can monitor all database connections.

    Password information is never returned.
    """


    connections = database.scalars(
        select(DatabaseConnection)
        .order_by(
            DatabaseConnection.created_at.desc()
        )
    ).all()



    return [

        {

            "id":
            connection.id,


            "user_id":
            connection.user_id,


            "connection_name":
            connection.connection_name,


            "database_name":
            connection.database_name,


            "host":
            connection.host,


            "status":
            (
                "active"
                if connection.is_active
                else
                "inactive"
            ),

        }

        for connection in connections

    ]









@router.get(
    "/stats",
    response_model=AdminStatsResponse,
)
def get_admin_stats(
    database: Session = Depends(get_app_db),
    current_user: User = Depends(require_owner),
):
    """
    Platform statistics.
    """


    total_users = database.scalar(
        select(
            func.count(User.id)
        )
    )



    total_connections = database.scalar(
        select(
            func.count(DatabaseConnection.id)
        )
    )



    total_queries = database.scalar(
        select(
            func.count(QueryHistory.id)
        )
    )



    return {

        "total_users":
        total_users,


        "total_connections":
        total_connections,


        "total_queries":
        total_queries,

    }