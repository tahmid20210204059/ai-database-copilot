from typing import Any

from pydantic import BaseModel


class SchemaResponse(BaseModel):
    """
    Structured database schema response
    used for AI context generation.
    """

    database: str

    tables: list[dict[str, Any]]

    relationships: list[dict[str, Any]]