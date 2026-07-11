from pydantic import BaseModel, Field


class AIQueryRequest(BaseModel):
    """
    User natural language query request.
    """

    prompt: str = Field(
        ...,
        min_length=3,
        max_length=2000,
        description="Natural language database question",
    )

    connection_id: int = Field(
        ...,
        gt=0,
        description="Selected database connection id",
    )



class AIGeneratedResponse(BaseModel):
    """
    Structured Gemini response.

    This schema represents AI generated SQL output.
    """

    sql: str = Field(
        ...,
        min_length=1,
        description="Generated SQL query",
    )


    summary: str = Field(
        ...,
        min_length=1,
        description="Explanation of generated SQL",
    )


    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="AI confidence score",
    )


    tables_used: list[str] = Field(
        default_factory=list,
        description="Tables used in SQL query",
    )


    read_only: bool = Field(
        default=True,
        description="Whether generated query is read only",
    )



class AIErrorResponse(BaseModel):
    """
    Standard AI error response.
    """

    error: str

    message: str