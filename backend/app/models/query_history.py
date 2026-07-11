from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    ForeignKey,
    Numeric,
    Text,
    Enum,
    func,
)

from ..database.base import Base



class QueryHistory(Base):
    """
    Stores user query execution history.
    """

    __tablename__ = "query_history"


    id = Column(
        BigInteger,
        primary_key=True,
        index=True,
        autoincrement=True,
    )


    user_id = Column(
        BigInteger,
        ForeignKey(
            "users.id"
        ),
        nullable=False,
        index=True,
    )


    connection_id = Column(
        BigInteger,
        ForeignKey(
            "db_connections.id"
        ),
        nullable=True,
        index=True,
    )


    prompt = Column(
        Text,
        nullable=False,
    )


    generated_sql = Column(
        Text,
        nullable=True,
    )


    explanation = Column(
        Text,
        nullable=True,
    )


    confidence = Column(
        Numeric(
            5,
            4,
        ),
        nullable=True,
    )


    execution_time_ms = Column(
        Numeric(
            12,
            3,
        ),
        nullable=True,
    )


    rows_returned = Column(
        BigInteger,
        nullable=False,
        default=0,
    )


    status = Column(
        Enum(
            "generated",
            "validated",
            "success",
            "failed",
            "rejected",
        ),
        nullable=False,
        default="generated",
        index=True,
    )


    error_message = Column(
        Text,
        nullable=True,
    )


    created_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        index=True,
    )