from backend.app.execution.query_executor import (
    query_executor,
)

from backend.app.validators.sql_validator import (
    sql_validator,
)

from backend.app.schemas.validation import (
    SQLValidationResult,
)

from backend.app.utils.encryption import (
    encryption_service,
)

from backend.app.database import app_engine

from sqlalchemy import text



HOST = "localhost"

PORT = 3306

DATABASE = "enterprise_sales"

USERNAME = "copilot_reader"



def get_password():

    with app_engine.connect() as connection:

        result = connection.execute(
            text(
                """
                SELECT encrypted_password
                FROM db_connections
                WHERE id=1
                """
            )
        )

        encrypted = result.scalar()


    return encryption_service.decrypt(
        encrypted
    )




PASSWORD = get_password()




def section(name):

    print("\n" + "=" * 70)

    print(name)

    print("=" * 70)




def test_select_execution():

    section(
        "1. SELECT EXECUTION TEST"
    )


    sql = """
    SELECT *
    FROM customers
    LIMIT 5
    """


    validation = sql_validator.validate(
        sql
    )


    result = query_executor.execute(

        validation,

        HOST,

        PORT,

        DATABASE,

        USERNAME,

        PASSWORD,

    )


    print(result)


    assert validation.is_valid is True

    assert result.success is True

    assert result.row_count <= 5




def test_join_execution():

    section(
        "2. JOIN EXECUTION TEST"
    )


    sql = """

    SELECT

    c.company_name,

    so.total_amount


    FROM customers c


    JOIN sales_orders so

    ON c.id = so.customer_id


    LIMIT 5

    """


    validation = sql_validator.validate(
        sql
    )


    result = query_executor.execute(

        validation,

        HOST,

        PORT,

        DATABASE,

        USERNAME,

        PASSWORD,

    )


    print(result)


    assert result.success is True




def test_cte_execution():

    section(
        "3. CTE EXECUTION TEST"
    )


    sql = """

    WITH temp AS (

        SELECT *

        FROM customers

        LIMIT 3

    )

    SELECT *

    FROM temp

    """


    validation = sql_validator.validate(
        sql
    )


    result = query_executor.execute(

        validation,

        HOST,

        PORT,

        DATABASE,

        USERNAME,

        PASSWORD,

    )


    print(result)


    assert result.success is True




def test_invalid_validation_block():

    section(
        "4. VALIDATION BLOCK TEST"
    )


    invalid = SQLValidationResult(

        is_valid=False,

        safe_sql=None,

        statement_type="DELETE",

        reason="Blocked",

        error_message="Not allowed",

    )


    result = query_executor.execute(

        invalid,

        HOST,

        PORT,

        DATABASE,

        USERNAME,

        PASSWORD,

    )


    print(result)


    assert result.success is False




def test_empty_result():

    section(
        "5. EMPTY RESULT TEST"
    )


    sql = """

    SELECT *

    FROM customers

    WHERE id=-999999

    """


    validation = sql_validator.validate(
        sql
    )


    result = query_executor.execute(

        validation,

        HOST,

        PORT,

        DATABASE,

        USERNAME,

        PASSWORD,

    )


    print(result)


    assert result.success is True

    assert result.row_count == 0




def test_database_error():

    section(
        "6. DATABASE ERROR TEST"
    )


    sql = """

    SELECT *

    FROM table_does_not_exist

    """


    validation = sql_validator.validate(
        sql
    )


    result = query_executor.execute(

        validation,

        HOST,

        PORT,

        DATABASE,

        USERNAME,

        PASSWORD,

    )


    print(result)


    assert result.success is False




def test_final():

    section(
        "FINAL RESULT"
    )


    print(
        "QUERY EXECUTION AUDIT PASSED"
    )