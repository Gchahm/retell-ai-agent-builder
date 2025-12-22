from datetime import datetime
from typing import Optional

from sqlmodel import JSON, Column, Field, SQLModel


class AgentConfig(SQLModel, table=True):
    """Agent configuration for voice calls."""

    __tablename__ = "agent_configurations"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    system_prompt: str
    scenario_type: str  # "check-in" or "emergency"

    # Retell settings stored as JSON
    retell_settings: dict = Field(default_factory=dict, sa_column=Column(JSON))

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
