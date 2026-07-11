from sqlalchemy import text

from ..database.dynamic_engine import create_dynamic_engine
from ..utils.encryption import encryption_service


class SchemaExtractionService:
    """
    Extract database metadata without reading actual table data.

    This service only reads:
    - Tables
    - Columns
    - Data types
    - Primary keys
    - Foreign keys
    - Relationships

    It never reads actual business data.
    """

    def extract_schema(
        self,
        host: str,
        port: int,
        database_name: str,
        username: str,
        encrypted_password: str,
    ) -> dict:
        """
        Main schema extraction workflow.
        """

        try:
            password = encryption_service.decrypt(
                encrypted_password
            )

            engine = create_dynamic_engine(
                host=host,
                port=port,
                database_name=database_name,
                username=username,
                password=password,
            )

            with engine.connect() as connection:

                tables = self._get_tables(
                    connection,
                    database_name,
                )

                columns = self._get_columns(
                    connection,
                    database_name,
                )

                primary_keys = self._get_primary_keys(
                    connection,
                    database_name,
                )

                foreign_keys = self._get_foreign_keys(
                    connection,
                    database_name,
                )

            return self._build_schema_response(
                database_name,
                tables,
                columns,
                primary_keys,
                foreign_keys,
            )

        except Exception as error:

            raise RuntimeError(
                f"Schema extraction failed: {str(error)}"
            )


    def _get_tables(
        self,
        connection,
        database_name: str,
    ) -> list[str]:
        """
        Get only real tables.
        Ignore database views.
        """

        query = text(
            """
            SELECT TABLE_NAME
            FROM information_schema.tables
            WHERE TABLE_SCHEMA = :database
            AND TABLE_TYPE = 'BASE TABLE'
            ORDER BY TABLE_NAME
            """
        )

        result = connection.execute(
            query,
            {
                "database": database_name
            },
        )

        return [
            row[0]
            for row in result.fetchall()
        ]


    def _get_columns(
        self,
        connection,
        database_name: str,
    ):
        """
        Get columns only from base tables.
        """

        query = text(
            """
            SELECT
                TABLE_NAME,
                COLUMN_NAME,
                DATA_TYPE
            FROM information_schema.columns
            WHERE TABLE_SCHEMA = :database
            AND TABLE_NAME IN
            (
                SELECT TABLE_NAME
                FROM information_schema.tables
                WHERE TABLE_SCHEMA = :database
                AND TABLE_TYPE = 'BASE TABLE'
            )
            ORDER BY TABLE_NAME, ORDINAL_POSITION
            """
        )

        result = connection.execute(
            query,
            {
                "database": database_name
            },
        )

        return result.fetchall()


    def _get_primary_keys(
        self,
        connection,
        database_name: str,
    ):
        """
        Detect primary keys.
        """

        query = text(
            """
            SELECT
                TABLE_NAME,
                COLUMN_NAME
            FROM information_schema.key_column_usage
            WHERE TABLE_SCHEMA = :database
            AND CONSTRAINT_NAME = 'PRIMARY'
            """
        )

        result = connection.execute(
            query,
            {
                "database": database_name
            },
        )

        return result.fetchall()


    def _get_foreign_keys(
        self,
        connection,
        database_name: str,
    ):
        """
        Detect foreign key relationships.
        """

        query = text(
            """
            SELECT
                TABLE_NAME,
                COLUMN_NAME,
                REFERENCED_TABLE_NAME,
                REFERENCED_COLUMN_NAME
            FROM information_schema.key_column_usage
            WHERE TABLE_SCHEMA = :database
            AND REFERENCED_TABLE_NAME IS NOT NULL
            """
        )

        result = connection.execute(
            query,
            {
                "database": database_name
            },
        )

        return result.fetchall()


    def _build_schema_response(
        self,
        database_name: str,
        tables,
        columns,
        primary_keys,
        foreign_keys,
    ) -> dict:
        """
        Convert raw metadata into AI-friendly JSON format.
        """

        schema_tables = {}

        for table in tables:

            schema_tables[table] = {
                "table_name": table,
                "columns": [],
                "primary_keys": [],
                "foreign_keys": [],
            }


        # Add columns

        for column in columns:

            table_name = column[0]

            if table_name not in schema_tables:
                continue


            schema_tables[table_name]["columns"].append(
                {
                    "name": column[1],
                    "type": column[2],
                    "primary_key": False,
                }
            )


        # Add primary keys

        for key in primary_keys:

            table_name = key[0]
            column_name = key[1]

            if table_name not in schema_tables:
                continue


            schema_tables[table_name]["primary_keys"].append(
                column_name
            )


        # Mark primary key columns

        for table in schema_tables.values():

            primary_columns = table["primary_keys"]

            for column in table["columns"]:

                if column["name"] in primary_columns:

                    column["primary_key"] = True



        relationships = []


        # Add foreign keys

        for fk in foreign_keys:

            table_name = fk[0]

            if table_name not in schema_tables:
                continue


            schema_tables[table_name]["foreign_keys"].append(
                {
                    "column": fk[1],
                    "references_table": fk[2],
                    "references_column": fk[3],
                }
            )


            relationships.append(
                {
                    "from":
                        f"{fk[0]}.{fk[1]}",

                    "to":
                        f"{fk[2]}.{fk[3]}",
                }
            )


        return {
            "database": database_name,

            "tables": list(
                schema_tables.values()
            ),

            "relationships": relationships,
        }



schema_service = SchemaExtractionService()