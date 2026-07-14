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
        description="Validated SQL ready for execution"
    )



    statement_type: str | None = Field(
        default=None,
        description="Detected SQL statement type"
    )



    reason: str = Field(
        default="",
        description="Validation decision reason"
    )



    error_message: str | None = Field(
        default=None,
        description="Human readable validation error"
    )



    blocked_keywords: list[str] = Field(
        default_factory=list,
        description="Restricted SQL keywords detected during validation"
    )



    validation_metadata: dict = Field(
        default_factory=dict,
        description="Additional validation information"
    )