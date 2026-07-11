from typing import Generator

from sqlalchemy import Engine, create_engine, text
from sqlalchemy.orm import Session, sessionmaker

from ..config import settings


# Application database engine
app_engine = create_engine(
    settings.APP_DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=1800,
)


# Reader database engine
reader_engine = create_engine(
    settings.READER_DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=1800,
)


AppSessionLocal = sessionmaker(
    bind=app_engine,
    autocommit=False,
    autoflush=False,
)


ReaderSessionLocal = sessionmaker(
    bind=reader_engine,
    autocommit=False,
    autoflush=False,
)


def get_app_db() -> Generator[Session, None, None]:
    database = AppSessionLocal()

    try:
        yield database

    finally:
        database.close()



def get_reader_db() -> Generator[Session, None, None]:
    database = ReaderSessionLocal()

    try:
        yield database

    finally:
        database.close()



def check_database_connection(
    engine: Engine,
) -> dict:

    try:

        with engine.connect() as connection:

            database_name = connection.execute(
                text("SELECT DATABASE()")
            ).scalar()

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