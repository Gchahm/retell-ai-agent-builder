from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Call(SQLModel, table=True):
    """Test call metadata."""

    __tablename__ = "test_calls"

    id: Optional[int] = Field(default=None, primary_key=True)

    # Retell agent ID (from Retell AI, not local database)
    retell_agent_id: str = Field(index=True)

    # Call details
    driver_name: str
    phone_number: str
    load_number: str

    # Status tracking
    status: str  # "pending", "in-progress", "completed", "failed"
    retell_call_id: Optional[str] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
