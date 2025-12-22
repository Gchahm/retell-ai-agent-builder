from pydantic import BaseModel, Field


class AgentCreateRequest(BaseModel):
    """Minimal request schema for creating a new agent via our API."""

    prompt: str = Field(
        ...,
        description="The system prompt that defines the agent's behavior and personality",
        min_length=1,
    )
    agent_name: str | None = Field(
        default=None,
        description="Optional name for the agent (for internal reference)",
    )
