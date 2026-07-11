# backend/app/database/dynamic_engine.py


from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine


def create_dynamic_engine(
    host: str,
    port: int,
    database_name: str,
    username: str,
    password: str,
) -> Engine:
    """
    User provided database-এর জন্য
    dynamic SQLAlchemy engine তৈরি করে।
    """

    connection_url = (
        f"mysql+pymysql://"
        f"{username}:{password}"
        f"@{host}:{port}/{database_name}"
    )

    engine = create_engine(
        connection_url,
        pool_pre_ping=True,
        pool_recycle=1800,
    )

    return engine



def test_database_connection(
    engine: Engine,
) -> dict:
    """
    Database connection test করে।
    """

    try:

        with engine.connect() as connection:

            database_name = connection.execute(
                text("SELECT DATABASE()")
            ).scalar()

        return {
            "success": True,
            "database": database_name,
            "message": "Database connection successful",
        }


    except Exception as error:

        return {
            "success": False,
            "database": None,
            "message": str(error),
        }