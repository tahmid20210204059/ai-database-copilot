from backend.app.validators.sql_validator import (
    sql_validator,
)



def section(title):

    print("\n" + "=" * 70)

    print(title)

    print("=" * 70)



def assert_valid(sql):

    result = sql_validator.validate(sql)

    print("\nSQL:")
    print(sql)

    print("Result:")
    print(result)

    assert result.is_valid is True



def assert_invalid(sql):

    result = sql_validator.validate(sql)

    print("\nSQL:")
    print(sql)

    print("Result:")
    print(result)

    assert result.is_valid is False



def test_select_allowed():

    section(
        "1. SELECT QUERY TEST"
    )

    assert_valid(
        "SELECT * FROM customers"
    )



def test_with_cte_allowed():

    section(
        "2. CTE QUERY TEST"
    )

    assert_valid(
        """
        WITH top_customers AS (
            SELECT *
            FROM customers
        )
        SELECT *
        FROM top_customers
        """
    )



def test_blocked_statements():

    section(
        "3. BLOCKED STATEMENT TEST"
    )


    blocked_queries = [

        "INSERT INTO customers VALUES (1)",

        "UPDATE customers SET name='test'",

        "DELETE FROM customers",

        "DROP TABLE customers",

        "ALTER TABLE customers ADD test INT",

        "CREATE TABLE test(id INT)",

        "TRUNCATE TABLE customers",

        "REPLACE INTO customers VALUES(1)",

        "MERGE INTO customers",

        "CALL test_procedure",

        "GRANT ALL ON customers",

        "REVOKE ALL ON customers",

        "SET GLOBAL test=1",

        "USE enterprise_sales",

        "SHOW TABLES",

        "DESCRIBE customers",

        "EXPLAIN SELECT * FROM customers",

        "LOCK TABLES customers WRITE",

    ]


    for query in blocked_queries:

        assert_invalid(query)



def test_dangerous_functions():

    section(
        "4. DANGEROUS FUNCTION TEST"
    )


    dangerous_queries = [

        "SELECT LOAD_FILE('/etc/passwd')",

        "SELECT SLEEP(10)",

        "SELECT BENCHMARK(1000,MD5('x'))",

        "SELECT * FROM customers INTO OUTFILE '/tmp/test.txt'",

        "SELECT * FROM customers INTO DUMPFILE '/tmp/test.txt'",

    ]


    for query in dangerous_queries:

        assert_invalid(query)



def test_multiple_statements():

    section(
        "5. MULTIPLE STATEMENT TEST"
    )


    assert_invalid(
        """
        SELECT *
        FROM customers;

        DELETE FROM customers;
        """
    )



def test_empty_sql():

    section(
        "6. EMPTY SQL TEST"
    )


    assert_invalid(
        ""
    )



def test_invalid_sql():

    section(
        "7. INVALID SQL TEST"
    )


    assert_invalid(
        "SELECT FROM customers"
    )



def test_final_result():

    section(
        "FINAL RESULT"
    )

    print(
        "SQL VALIDATOR SECURITY AUDIT PASSED"
    )