from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from retell.types import AgentListResponse, AgentResponse

from app.services.retell import RetellService

router = APIRouter(prefix="/api/agent-configs", tags=["agent-configs"])


def get_retell_service() -> RetellService:
    """Dependency to get RetellService instance."""
    return RetellService()


RetellServiceDep = Annotated[RetellService, Depends(get_retell_service)]


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


# The following endpoints are deprecated as we're not storing agents locally anymore
# Create, Update, and Delete should be done through Retell's dashboard or their API directly
