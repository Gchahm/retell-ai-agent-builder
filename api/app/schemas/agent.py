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


class AgentUpdateRequest(BaseModel):
    """Minimal request schema for updating an existing agent via our API."""

    prompt: str | None = Field(
        default=None,
        description="Updated system prompt (creates a new LLM and updates the agent)",
        min_length=1,
    )
    agent_name: str | None = Field(
        default=None,
        description="Updated name for the agent (for internal reference)",
    )


class AgentGetResponse(BaseModel):
    """Response schema for retrieving a single agent."""

    agent_id: str = Field(..., description="Unique identifier for the agent")
    name: str | None = Field(None, description="Name of the agent (for internal reference)")
    prompt: str | None = Field(None, description="The system prompt defining agent behavior")
