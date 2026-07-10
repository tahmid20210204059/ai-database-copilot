from typing import Generator

from sqlalchemy import Engine, create_engine, text
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from .config import settings


# FastAPI application database engine
# users, history, favorites, cache ইত্যাদির জন্য
app_engine = create_engine(
    settings.APP_DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=1800,
)


# AI-generated read-only query চালানোর database engine
reader_engine = create_engine(
    settings.READER_DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=1800,
)


# Application database session
AppSessionLocal = sessionmaker(
    bind=app_engine,
    autocommit=False,
    autoflush=False,
)


# Reader database session
ReaderSessionLocal = sessionmaker(
    bind=reader_engine,
    autocommit=False,
    autoflush=False,
)


# ভবিষ্যতে SQLAlchemy models তৈরিতে এটি ব্যবহার হবে
Base = declarative_base()


def get_app_db() -> Generator[Session, None, None]:
    """Application database session provide করবে."""

    database = AppSessionLocal()

    try:
        yield database
    finally:
        database.close()


def get_reader_db() -> Generator[Session, None, None]:
    """Read-only company database session provide করবে."""

    database = ReaderSessionLocal()

    try:
        yield database
    finally:
        database.close()


def check_database_connection(engine: Engine) -> dict:
    """Database connection test করে status return করবে."""

    try:
        with engine.connect() as connection:
            database_name = connection.execute(
                text("SELECT DATABASE()")
            ).scalar_one_or_none()

            connection.execute(text("SELECT 1"))

        return {
            "status": "connected",
            "database": database_name,
        }

    except Exception as error:
        return {
            "status": "disconnected",
            "database": None,
            "error": str(error),
        }