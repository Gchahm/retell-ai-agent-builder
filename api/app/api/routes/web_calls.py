from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.schemas import WebCallCreateRequest
from app.services.retell import RetellService

router = APIRouter(prefix="/api/web-calls", tags=["web-calls"])


def get_retell_service() -> RetellService:
    """Dependency to get RetellService instance."""
    return RetellService()


RetellServiceDep = Annotated[RetellService, Depends(get_retell_service)]


@router.post("", status_code=201)
def create_web_call(request: WebCallCreateRequest, retell_service: RetellServiceDep):
    """
    Create a web call via Retell AI.

    This endpoint creates a web call and returns an access token that can be used
    by the frontend to join the call.

    Args:
        request: Web call creation request with agent_id and optional metadata

    Returns:
        Call object from Retell SDK containing access_token and call details
    """
    try:
        return retell_service.create_web_call(
            agent_id=request.agent_id,
            metadata=request.metadata,
            retell_llm_dynamic_variables=request.retell_llm_dynamic_variables,
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to create web call in Retell: {str(e)}"
        ) from e
