class AIServiceError(Exception):
    """
    Base AI service exception.
    """



class AIRateLimitError(AIServiceError):
    """
    Raised when AI quota is exceeded.
    """

    retry_after_seconds = 60




class AITimeoutError(AIServiceError):
    """
    Raised when AI request timeout occurs.
    """




class AIResponseError(AIServiceError):
    """
    Raised when AI response is invalid.
    """