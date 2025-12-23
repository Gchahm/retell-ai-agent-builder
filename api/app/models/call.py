from datetime import datetime

from sqlmodel import Field, SQLModel


class Call(SQLModel, table=True):
    """Test call metadata."""

    __tablename__ = "test_calls"

    id: str = Field(primary_key=True)  # Retell call ID

    # Retell agent ID (from Retell AI, not local database)
    agent_id: str = Field(index=True)

    # Call details
    driver_name: str
    phone_number: str
    load_number: str

    # Status tracking
    status: str  # "pending", "in-progress", "completed", "failed"

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
