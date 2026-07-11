import logging
from typing import Final

import sqlglot
from sqlglot import exp


from ..schemas.validation import SQLValidationResult



logger = logging.getLogger(__name__)




class SQLValidator:
    """
    Production SQL security validator.

    Responsibilities:
    - Parse SQL safely
    - Detect statement type
    - Validate SQL structure
    - Apply security policy
    - Return validation result

    Does NOT:
    - Execute SQL
    - Access database
    - Modify SQL
    """



    ALLOWED_STATEMENTS: Final = {
        "SELECT",
        "WITH",
    }



    BLOCKED_STATEMENTS: Final = {

        "INSERT",
        "UPDATE",
        "DELETE",
        "DROP",
        "ALTER",
        "CREATE",
        "TRUNCATE",
        "RENAME",
        "REPLACE",
        "MERGE",
        "CALL",
        "EXECUTE",
        "GRANT",
        "REVOKE",
        "SET",
        "USE",
        "SHOW",
        "DESCRIBE",
        "EXPLAIN",
        "LOCK",
        "UNLOCK",
    }



    BLOCKED_FUNCTIONS: Final = {

        "LOAD_FILE",

        "BENCHMARK",

        "SLEEP",

    }



    BLOCKED_KEYWORDS: Final = {

        "INTO OUTFILE",

        "INTO DUMPFILE",

    }



    def validate(
        self,
        sql: str,
    ) -> SQLValidationResult:
        """
        Validate generated SQL.
        """


        try:

            if not sql or not sql.strip():

                return self._reject(
                    reason="Empty SQL query",
                    error="SQL cannot be empty",
                )



            statements = sqlglot.parse(
                sql,
                read="mysql",
            )


            if len(statements) != 1:

                return self._reject(
                    reason="Multiple SQL statements detected",
                    error="Only one SQL statement is allowed",
                )



            expression = statements[0]



            statement_type = (
                self._detect_statement_type(
                    expression
                )
            )



            if statement_type not in self.ALLOWED_STATEMENTS:

                return self._reject(
                    statement_type=statement_type,

                    reason="Blocked SQL statement type",

                    error=f"{statement_type} is not allowed",
                )



            if not self._validate_query_structure(
                expression
            ):

                return self._reject(
                    statement_type=statement_type,

                    reason="Invalid SQL structure",

                    error="SQL structure validation failed",
                )



            sql_upper = sql.upper()



            for keyword in self.BLOCKED_KEYWORDS:

                if keyword in sql_upper:

                    return self._reject(
                        statement_type=statement_type,

                        reason="Dangerous SQL keyword detected",

                        error=f"{keyword} is not allowed",
                    )



            for function in self.BLOCKED_FUNCTIONS:

                if function in sql_upper:

                    return self._reject(
                        statement_type=statement_type,

                        reason="Dangerous SQL function detected",

                        error=f"{function} is not allowed",
                    )



            logger.info(
                "SQL validation successful"
            )


            return SQLValidationResult(

                is_valid=True,

                safe_sql=sql.strip(),

                statement_type=statement_type,

                reason="SQL passed validation",

                error_message=None,
            )



        except sqlglot.errors.ParseError:

            logger.warning(
                "SQL parsing failed"
            )


            return self._reject(
                reason="Invalid SQL syntax",

                error="SQL could not be parsed",
            )



        except Exception as error:


            logger.error(
                "Unexpected SQL validation error: %s",
                error,
            )


            return self._reject(
                reason="SQL validation failed",

                error="Unexpected validation error",
            )




    def _validate_query_structure(
        self,
        expression: exp.Expression,
    ) -> bool:
        """
        Validate SQL AST structure.

        Prevents malformed SQL
        accepted by parser.
        """



        if isinstance(
            expression,
            exp.Select,
        ):

            if not expression.expressions:

                return False



        return True




    def _detect_statement_type(
        self,
        expression: exp.Expression,
    ) -> str:
        """
        Detect SQL operation type.
        """



        if isinstance(
            expression,
            exp.Select,
        ):

            return "SELECT"



        if isinstance(
            expression,
            exp.With,
        ):

            return "WITH"



        return expression.key.upper()




    def _reject(
        self,
        reason: str,
        error: str,
        statement_type: str | None = None,
    ) -> SQLValidationResult:
        """
        Create rejection response.
        """



        logger.warning(
            "SQL rejected: %s",
            reason,
        )



        return SQLValidationResult(

            is_valid=False,

            safe_sql=None,

            statement_type=statement_type,

            reason=reason,

            error_message=error,
        )




sql_validator = SQLValidator()