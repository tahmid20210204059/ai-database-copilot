# backend/app/api/routes/query.py


from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)


from sqlalchemy.orm import Session



from ...database import (
    get_app_db,
)


from ...auth.permissions import (
    require_user,
)


from ...models.user import (
    User,
)


from ...models.connection import (
    DatabaseConnection,
)


from ...schemas.execution import (
    QueryExecutionRequest,
    QueryExecutionResponse,
)


from ...schemas.validation import (
    SQLValidationResult,
)


from ...schemas.history import (
    HistoryCreate,
)


from ...execution.query_executor import (
    query_executor,
)


from ...services.history_service import (
    history_service,
)


from ...validators.sql_validator import (
    sql_validator,
)





router = APIRouter(
    prefix="/api/query",
    tags=["Query Execution"],
)









@router.post(
    "/execute",
    response_model=QueryExecutionResponse,
    status_code=status.HTTP_200_OK,
)
def execute_query(
    data: QueryExecutionRequest,

    db: Session = Depends(
        get_app_db
    ),

    current_user: User = Depends(
        require_user
    ),
):
    """
    Execute validated SQL query.

    Flow:

    User SQL
        ↓
    Validate SQL
        ↓
    Execute Query
        ↓
    Save History
        ↓
    Return Result
    """



    connection = (

        db.query(
            DatabaseConnection
        )

        .filter(

            DatabaseConnection.id
            ==
            data.connection_id,


            DatabaseConnection.user_id
            ==
            current_user.id,

        )

        .first()

    )





    if not connection:


        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND,

            detail="Database connection not found",

        )








    validation_result: SQLValidationResult = (

        sql_validator.validate(

            data.sql

        )

    )









    result = query_executor.execute(

        validation_result=validation_result,

        host=connection.host,

        port=connection.port,

        database_name=connection.database_name,

        username=connection.username,

        password=connection.get_password(),

    )









    history_status = (

        "success"

        if result.success

        else

        "failed"

    )








    history_data = HistoryCreate(

        connection_id=data.connection_id,

        prompt="SQL execution",

        generated_sql=result.sql_executed,

        execution_time_ms=result.execution_time_ms,

        rows_returned=result.row_count,

        status=history_status,

        error_message=

        None

        if result.success

        else result.message,

    )







    try:


        history_service.create_history(

            db=db,

            user_id=current_user.id,

            data=history_data,

        )


    except Exception:


        pass







    return result