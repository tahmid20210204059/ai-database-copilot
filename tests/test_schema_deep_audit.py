import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(
    0,
    str(PROJECT_ROOT)
)


from sqlalchemy import text

from backend.app.database import app_engine

from backend.app.services.schema_service import (
    schema_service,
)

from backend.app.models.connection import (
    DatabaseConnection,
)

from backend.app.utils.encryption import (
    encryption_service,
)


def print_section(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)



def test_schema_internal_audit():

    print_section(
        "1. APPLICATION DATABASE CHECK"
    )


    with app_engine.connect() as connection:

        row = connection.execute(
            text(
                """
                SELECT
                    id,
                    database_name,
                    username,
                    encrypted_password
                FROM db_connections
                WHERE id = 1
                """
            )
        ).fetchone()


    assert row is not None


    connection_id = row[0]

    database_name = row[1]

    username = row[2]

    encrypted_password = row[3]


    print(
        "Connection ID:",
        connection_id
    )

    print(
        "Database:",
        database_name
    )

    print(
        "Username:",
        username
    )


    assert encrypted_password.startswith(
        "gAAAA"
    )


    print(
        "Password encryption: PASS"
    )



    print_section(
        "2. PASSWORD DECRYPT TEST"
    )


    password = encryption_service.decrypt(
        encrypted_password
    )


    print(
        "Password decrypted successfully"
    )


    assert password != encrypted_password



    print_section(
        "3. SCHEMA EXTRACTION TEST"
    )


    schema = schema_service.extract_schema(

        host="localhost",

        port=3306,

        database_name=database_name,

        username=username,

        encrypted_password=encrypted_password,
    )


    assert schema["database"] == database_name


    print(
        "Database:",
        schema["database"]
    )


    tables = schema["tables"]

    relationships = schema["relationships"]


    print(
        "Table count:",
        len(tables)
    )


    print(
        "Relationship count:",
        len(relationships)
    )


    assert len(tables) > 0



    print_section(
        "4. TABLE STRUCTURE CHECK"
    )


    table_names = [
        table["table_name"]
        for table in tables
    ]


    print(
        table_names
    )


    required_tables = [

        "customers",
        "products",
        "sales_orders",
        "order_items"

    ]


    for table in required_tables:

        assert table in table_names


    print(
        "Required tables exist: PASS"
    )



    print_section(
        "5. COLUMN METADATA CHECK"
    )


    customers = next(

        table

        for table in tables

        if table["table_name"] == "customers"

    )


    columns = [

        column["name"]

        for column in customers["columns"]

    ]


    print(
        "Customer columns:",
        columns
    )


    assert "id" in columns

    assert "company_name" in columns


    print(
        "Column extraction: PASS"
    )



    print_section(
        "6. PRIMARY KEY CHECK"
    )


    assert "id" in customers["primary_keys"]


    print(
        "Primary key detection: PASS"
    )



    print_section(
        "7. FOREIGN KEY CHECK"
    )


    relationship_exists = False


    for relation in relationships:

        if (

            relation["from"]
            ==
            "sales_orders.customer_id"

            and

            relation["to"]
            ==
            "customers.id"

        ):

            relationship_exists = True



    assert relationship_exists


    print(
        "Foreign key detection: PASS"
    )



    print_section(
        "8. SECURITY CHECK"
    )


    schema_text = str(schema)


    assert "password" not in schema_text.lower()

    assert "encrypted_password" not in schema_text.lower()


    print(
        "No credential leakage: PASS"
    )



    print_section(
        "FINAL RESULT"
    )


    print(
        "SCHEMA EXTRACTION MODULE AUDIT PASSED"
    )