
from fastapi import APIRouter, HTTPException, Query
from retell.types import AgentListResponse, AgentResponse

from app.api.deps import CurrentUserDep, RetellServiceDep
from app.schemas import AgentCreateRequest, AgentGetResponse, AgentUpdateRequest
from app.services.prompts import get_initial_prompt_template

router = APIRouter(prefix="/api/agent-configs", tags=["agent-configs"])


@router.get("/initial-prompt")
def get_initial_prompt(user: CurrentUserDep) -> dict[str, str]:
    """
    Get the initial prompt template for creating new agents.

    Returns the portion of the system prompt that comes after the style
    guardrails, which can be used as a starting point for custom prompts.

    Returns:
        dict with "prompt" key containing the initial template
    """
    return {"prompt": get_initial_prompt_template()}


@router.post("", response_model=AgentResponse, status_code=201)
def create_agent_config(
    request: AgentCreateRequest, retell_service: RetellServiceDep, user: CurrentUserDep
):
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
    user: CurrentUserDep,
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


@router.get("/{agent_id}", response_model=AgentGetResponse)
def get_agent_config(agent_id: str, retell_service: RetellServiceDep, user: CurrentUserDep):
    """
    Get a specific agent configuration from Retell AI.

    This endpoint returns only the essential agent details: agent_id, name, and prompt.

    Args:
        agent_id: The ID of the agent to retrieve

    Returns:
        AgentGetResponse with agent_id, name, and prompt
    """
    try:
        return retell_service.get_agent(agent_id)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to fetch agent from Retell: {str(e)}"
        ) from e


@router.patch("/{agent_id}", response_model=AgentResponse)
def update_agent_config(
    agent_id: str,
    request: AgentUpdateRequest,
    retell_service: RetellServiceDep,
    user: CurrentUserDep,
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
