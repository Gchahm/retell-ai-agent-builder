from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from retell.types import AgentListResponse, AgentResponse

from app.schemas import AgentCreateRequest, AgentUpdateRequest
from app.services.retell import RetellService

router = APIRouter(prefix="/api/agent-configs", tags=["agent-configs"])


def get_retell_service() -> RetellService:
    """Dependency to get RetellService instance."""
    return RetellService()


RetellServiceDep = Annotated[RetellService, Depends(get_retell_service)]


@router.post("", response_model=AgentResponse, status_code=201)
def create_agent_config(request: AgentCreateRequest, retell_service: RetellServiceDep):
    """
    Create a new agent configuration in Retell AI.

    This is a light wrapper that creates an agent with sensible defaults.
    You only need to provide the prompt text - all other configuration
    (voice, model, responsiveness, etc.) is handled by our API.

    Args:
        request: Agent creation request with prompt and optional name

    Returns:
        AgentResponse: The created agent from Retell SDK
    """
    try:
        return retell_service.create_agent(prompt=request.prompt, agent_name=request.agent_name)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to create agent in Retell: {str(e)}"
        ) from e


@router.get("", response_model=AgentListResponse)
def list_agent_configs(
    retell_service: RetellServiceDep,
    limit: int = Query(default=1000, ge=1, le=1000),
    pagination_key: str | None = Query(default=None),
):
    """
    List all agent configurations from Retell AI.

    Args:
        limit: Number of agents to return (1-1000, default 1000)
        pagination_key: Agent ID to continue fetching from (for pagination)

    Returns:
        List of AgentResponse objects from Retell SDK
    """
    try:
        return retell_service.list_agents(limit=limit, pagination_key=pagination_key)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to fetch agents from Retell: {str(e)}"
        ) from e


@router.get("/{agent_id}", response_model=AgentResponse)
def get_agent_config(agent_id: str, retell_service: RetellServiceDep):
    """
    Get a specific agent configuration from Retell AI.

    Note: This endpoint requires implementing the get_agent method in RetellService.
    """
    # TODO: Implement get_agent in RetellService
    raise HTTPException(
        status_code=501,
        detail="Get single agent not yet implemented. Use list endpoint with pagination.",
    )


@router.patch("/{agent_id}", response_model=AgentResponse)
def update_agent_config(
    agent_id: str, request: AgentUpdateRequest, retell_service: RetellServiceDep
):
    """
    Update an existing agent configuration in Retell AI.

    This is a light wrapper that allows updating:
    - The prompt (creates a new LLM and updates the agent's response_engine)
    - The agent name

    At least one field must be provided.

    Args:
        agent_id: The ID of the agent to update
        request: Agent update request with optional prompt and/or agent_name

    Returns:
        AgentResponse: The updated agent from Retell SDK
    """
    # Validate that at least one field is provided
    if request.prompt is None and request.agent_name is None:
        raise HTTPException(
            status_code=422,
            detail="At least one field (prompt or agent_name) must be provided for update",
        )

    try:
        return retell_service.update_agent(
            agent_id=agent_id, prompt=request.prompt, agent_name=request.agent_name
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to update agent in Retell: {str(e)}"
        ) from e


# Delete should be done through Retell's dashboard or their API directly
