from datetime import datetime
from typing import Optional

from sqlmodel import JSON, Column, Field, SQLModel


class CallResult(SQLModel, table=True):
    """Call results and structured data."""

    __tablename__ = "call_results"

    id: Optional[int] = Field(default=None, primary_key=True)
    call_id: int = Field(foreign_key="test_calls.id")

    # Raw data
    transcript: str

    # Structured data (varies by scenario)
    structured_data: dict = Field(default_factory=dict, sa_column=Column(JSON))

    created_at: datetime = Field(default_factory=datetime.utcnow)
