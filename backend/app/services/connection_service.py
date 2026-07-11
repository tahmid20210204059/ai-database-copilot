from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database.dynamic_engine import (
    create_dynamic_engine,
    test_database_connection,
)

from ..models.connection import DatabaseConnection

from ..utils.encryption import encryption_service


class ConnectionService:
    """
    Handles database connection operations.
    """

    def test_connection(
        self,
        host: str,
        port: int,
        database_name: str,
        username: str,
        password: str,
    ) -> dict:
        """
        Test external database connection.
        """

        engine = create_dynamic_engine(
            host=host,
            port=port,
            database_name=database_name,
            username=username,
            password=password,
        )

        return test_database_connection(engine)


    def create_connection(
        self,
        database: Session,
        user_id: int,
        connection_data,
    ):
        """
        Save user database connection.
        Password will be encrypted.
        """

        encrypted_password = (
            encryption_service.encrypt(
                connection_data.password
            )
        )


        new_connection = DatabaseConnection(
            user_id=user_id,
            connection_name=connection_data.connection_name,
            host=connection_data.host,
            port=connection_data.port,
            database_name=connection_data.database_name,
            username=connection_data.username,
            encrypted_password=encrypted_password,
            ssl_enabled=connection_data.ssl_enabled,
            last_tested_at=datetime.now(),
        )


        database.add(new_connection)

        database.commit()

        database.refresh(new_connection)

        return new_connection


    def get_user_connections(
        self,
        database: Session,
        user_id: int,
    ):
        """
        Return only current user's connections.
        """

        query = (
            select(DatabaseConnection)
            .where(
                DatabaseConnection.user_id == user_id
            )
            .order_by(
                DatabaseConnection.created_at.desc()
            )
        )

        return database.scalars(query).all()



    def delete_connection(
        self,
        database: Session,
        connection_id: int,
        user_id: int,
    ):
        """
        Delete connection only if it belongs
        to current user.
        """

        query = (
            select(DatabaseConnection)
            .where(
                DatabaseConnection.id == connection_id,
                DatabaseConnection.user_id == user_id,
            )
        )


        connection = database.scalar(query)


        if connection is None:
            return False


        database.delete(connection)

        database.commit()


        return True



connection_service = ConnectionService()