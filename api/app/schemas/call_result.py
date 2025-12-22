from datetime import datetime

from pydantic import BaseModel


class CallResultResponse(BaseModel):
    """Schema for call result response."""

    id: int
    call_id: int
    transcript: str
    structured_data: dict
    created_at: datetime

    model_config = {"from_attributes": True}
