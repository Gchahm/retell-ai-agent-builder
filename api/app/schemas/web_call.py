from pydantic import BaseModel, Field


class WebCallCreateRequest(BaseModel):
    """Schema for creating a web call."""

    agent_id: str = Field(..., description="Unique ID of agent used for the call")
    metadata: dict | None = Field(
        None,
        description="Arbitrary key-value storage for internal use (e.g., customer IDs)",
    )
    retell_llm_dynamic_variables: dict[str, str] | None = Field(
        None,
        description="Dynamic string variables to inject into prompt and tool descriptions",
    )
