from datetime import datetime

from pydantic import BaseModel, Field


class ConnectionCreate(BaseModel):

    connection_name: str = Field(
        min_length=2,
        max_length=120
    )

    host: str

    port: int = 3306

    database_name: str

    username: str

    password: str

    ssl_enabled: bool = False



class ConnectionResponse(BaseModel):

    id: int

    connection_name: str

    host: str

    port: int

    database_name: str

    username: str

    ssl_enabled: bool

    is_active: bool

    last_tested_at: datetime | None

    created_at: datetime