from datetime import datetime

from pydantic import BaseModel


class CallCreate(BaseModel):
    """Schema for triggering a call."""

    agent_id: str
    driver_name: str
    phone_number: str
    load_number: str


class CallResponse(BaseModel):
    """Schema for call response."""

    id: str  # Retell call ID
    agent_id: str
    driver_name: str
    phone_number: str
    load_number: str
    status: str
    created_at: datetime
    updated_at: datetime
    transcript: str | None = None
    structured_data: dict | None = None

    model_config = {"from_attributes": True}
