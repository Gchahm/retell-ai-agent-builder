from datetime import datetime

from pydantic import BaseModel


class AgentConfigCreate(BaseModel):
    """Schema for creating agent configuration."""

    name: str
    system_prompt: str
    scenario_type: str
    retell_settings: dict = {}


class AgentConfigUpdate(BaseModel):
    """Schema for updating agent configuration."""

    name: str | None = None
    system_prompt: str | None = None
    scenario_type: str | None = None
    retell_settings: dict | None = None


class AgentConfigResponse(BaseModel):
    """Schema for agent configuration response."""

    id: int
    name: str
    system_prompt: str
    scenario_type: str
    retell_settings: dict
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
