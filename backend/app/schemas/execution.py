from typing import Any

from pydantic import BaseModel, Field



class QueryExecutionRequest(BaseModel):
    """
    Request payload for executing validated SQL.
    """

    connection_id: int = Field(
        description="User owned database connection id"
    )


    sql: str = Field(
        description="SQL query to execute"
    )






class QueryExecutionResponse(BaseModel):
    """
    Structured response returned after SQL execution.
    """

    success: bool = Field(
        description="Execution status"
    )



    sql_executed: str | None = Field(
        default=None,
        description="Executed validated SQL"
    )



    columns: list[str] = Field(
        default_factory=list,
        description="Returned column names"
    )



    rows: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Query result rows"
    )



    row_count: int = Field(
        default=0,
        description="Number of returned rows"
    )



    execution_time_ms: float = Field(
        default=0.0,
        description="Execution duration in milliseconds"
    )



    message: str = Field(
        default="",
        description="Execution result message"
    )



    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional execution metadata"
    )