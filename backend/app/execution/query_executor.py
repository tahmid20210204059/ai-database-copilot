import logging
import time
from typing import Any


from sqlalchemy import text


from ..database.dynamic_engine import create_dynamic_engine

from ..schemas.execution import QueryExecutionResponse

from ..schemas.validation import SQLValidationResult



logger = logging.getLogger(__name__)





class QueryExecutionError(Exception):
    """
    Query execution related exception.
    """






class QueryExecutor:
    """
    Executes validated read-only SQL queries.

    Responsibilities:
    - Execute validated SELECT queries
    - Create dynamic database connection
    - Format query results
    - Track execution performance

    Does NOT:
    - Generate SQL
    - Validate SQL
    - Modify SQL
    - Handle Gemini operations
    """






    def execute(
        self,
        validation_result: SQLValidationResult,
        host: str,
        port: int,
        database_name: str,
        username: str,
        password: str,
    ) -> QueryExecutionResponse:
        """
        Execute a validated SQL query.
        """



        start_time = time.perf_counter()





        if not validation_result.is_valid:

            logger.warning(
                "Query execution blocked. SQL validation failed."
            )


            return QueryExecutionResponse(

                success=False,

                sql_executed=None,

                message="SQL validation failed",

                metadata={

                    "reason":
                    validation_result.reason

                },

            )







        sql = validation_result.safe_sql





        if not sql:

            return QueryExecutionResponse(

                success=False,

                sql_executed=None,

                message="No SQL query provided",

                metadata={},

            )








        engine = None



        try:


            logger.info(
                "Starting query execution."
            )





            engine = create_dynamic_engine(

                host=host,

                port=port,

                database_name=database_name,

                username=username,

                password=password,

            )







            with engine.connect() as connection:


                result = connection.execute(
                    text(sql)
                )



                rows = result.fetchall()



                columns = list(
                    result.keys()
                )







            formatted_rows = [

                dict(row._mapping)

                for row in rows

            ]






            execution_time = (

                time.perf_counter()

                -

                start_time

            ) * 1000







            logger.info(

                "Query completed successfully. Time: %.3f ms",

                execution_time,

            )







            return QueryExecutionResponse(

                success=True,

                sql_executed=sql,

                columns=columns,

                rows=formatted_rows,

                row_count=len(
                    formatted_rows
                ),

                execution_time_ms=

                    round(

                        execution_time,

                        3,

                    ),


                message="Query executed successfully",


                metadata={

                    "database":
                    database_name,

                    "execution_type":
                    "read_only",

                },

            )








        except Exception as error:



            execution_time = (

                time.perf_counter()

                -

                start_time

            ) * 1000





            logger.exception(

                "Query execution failed: %s",

                error,

            )






            return QueryExecutionResponse(

                success=False,

                sql_executed=sql,

                columns=[],

                rows=[],

                row_count=0,

                execution_time_ms=

                    round(

                        execution_time,

                        3,

                    ),


                message="Query execution failed",


                metadata={

                    "database":
                    database_name,

                    "error":
                    str(error),

                },

            )







        finally:


            if engine:

                engine.dispose()







query_executor = QueryExecutor()