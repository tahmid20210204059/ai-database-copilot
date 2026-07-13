from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
)





class AdminUserResponse(BaseModel):
    """
    Owner view of application users.
    """


    model_config = ConfigDict(
        from_attributes=True
    )


    id: int

    name: str

    email: str

    role: str

    is_active: bool

    created_at: datetime





class AdminConnectionResponse(BaseModel):
    """
    Owner view of connected databases.

    Password information excluded.
    """


    id: int

    user_id: int

    connection_name: str

    database_name: str

    host: str

    status: str





class AdminStatsResponse(BaseModel):
    """
    Platform statistics.
    """


    total_users: int

    total_connections: int

    total_queries: int