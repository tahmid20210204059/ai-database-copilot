from datetime import datetime

from pydantic import BaseModel, Field





class HistoryCreate(BaseModel):
    """
    Data required to create query history.
    """



    connection_id: int | None = Field(
        default=None,
        description="Database connection id",
    )



    prompt: str = Field(
        min_length=3,
        max_length=5000,
        description="User natural language prompt",
    )



    generated_sql: str | None = Field(
        default=None,
        description="Generated SQL query",
    )



    explanation: str | None = Field(
        default=None,
        description="AI SQL explanation",
    )



    confidence: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="AI confidence score",
    )



    execution_time_ms: float | None = Field(
        default=None,
        description="Query execution duration in milliseconds",
    )



    rows_returned: int = Field(
        default=0,
        ge=0,
        description="Number of returned rows",
    )



    status: str = Field(
        default="generated",
        description="Query lifecycle status",
    )



    error_message: str | None = Field(
        default=None,
        description="Execution error message",
    )







class HistoryResponse(BaseModel):
    """
    Query history API response.
    """



    id: int



    connection_id: int | None



    prompt: str



    generated_sql: str | None



    explanation: str | None



    confidence: float | None



    execution_time_ms: float | None



    rows_returned: int



    status: str



    error_message: str | None



    created_at: datetime





    class Config:

        from_attributes = True







class HistoryFilter(BaseModel):
    """
    Query history filtering options.
    """



    status: str | None = None



    connection_id: int | None = None







class HistoryListResponse(BaseModel):
    """
    Paginated query history response.
    """



    items: list[HistoryResponse]



    page: int



    page_size: int



    total: int