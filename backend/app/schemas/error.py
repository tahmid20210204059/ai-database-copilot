from pydantic import BaseModel


class APIErrorResponse(BaseModel):
    """
    Standard API error response.
    """

    error_code: str

    message: str

    retry_after_seconds: int | None = None