from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    SmallInteger,
    String,
    Text,
    func,
    text,
)

from sqlalchemy.orm import Mapped, mapped_column

from ..database.base import Base


class DatabaseConnection(Base):

    __tablename__ = "db_connections"


    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )


    user_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        index=True
    )


    connection_name: Mapped[str] = mapped_column(
        String(120),
        nullable=False
    )


    host: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )


    port: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False,
        server_default="3306"
    )


    database_name: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
        index=True
    )


    username: Mapped[str] = mapped_column(
        String(120),
        nullable=False
    )


    encrypted_password: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )


    ssl_enabled: Mapped[bool] = mapped_column(
        Boolean,
        server_default=text("0")
    )


    is_active: Mapped[bool] = mapped_column(
        Boolean,
        server_default=text("1")
    )


    last_tested_at: Mapped[datetime | None]


    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )


    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )