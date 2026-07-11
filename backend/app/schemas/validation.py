from pydantic import BaseModel, Field


class SQLValidationResult(BaseModel):
    """
    Result returned after SQL security validation.
    """

    is_valid: bool = Field(
        description="Whether SQL is safe to execute"
    )


    safe_sql: str | None = Field(
        default=None,
        description="Original SQL after validation"
    )


    statement_type: str | None = Field(
        default=None,
        description="Detected SQL statement type"
    )


    reason: str = Field(
        description="Validation reason"
    )


    error_message: str | None = Field(
        default=None,
        description="Human readable validation error"
    )