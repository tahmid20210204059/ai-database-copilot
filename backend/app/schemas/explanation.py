from pydantic import BaseModel, Field



class SQLExplanationRequest(BaseModel):
    """
    Request schema for SQL explanation.
    """


    sql: str = Field(
        min_length=1,
        description="SQL query to explain",
    )



    context: str | None = Field(
        default=None,
        description="Optional database context",
    )





class SQLExplanationResponse(BaseModel):
    """
    AI generated SQL explanation response.
    """


    explanation: str = Field(
        description="Human readable explanation",
    )


    key_points: list[str] = Field(
        default_factory=list,
        description="Important explanation points",
    )


    complexity: str = Field(
        default="unknown",
        description="Query complexity level",
    )