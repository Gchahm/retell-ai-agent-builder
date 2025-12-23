from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.api.deps import RetellServiceDep, SessionDep
from app.models import Call
from app.schemas import CallCreate, CallResponse

router = APIRouter(prefix="/api/calls", tags=["calls"])


@router.post("webcall/", status_code=201)
def create_web_call(request: CallCreate, retell_service: RetellServiceDep, session: SessionDep):
    """
    Create a web call via Retell AI.

    This endpoint creates a web call and returns an access token that can be used
    by the frontend to join the call. The driver_name, phone_number, and load_number
    are automatically injected as dynamic variables into the agent's prompt.

    Args:
        request: Web call creation request with agent_id, driver info, and load details

    Returns:
        Call object from Retell SDK containing access_token and call details
    """
    try:
        db_call = Call(
            retell_agent_id=request.retell_agent_id,
            driver_name=request.driver_name,
            phone_number=request.phone_number,
            load_number=request.load_number,
            status="pending",
        )

        session.add(db_call)
        session.commit()
        session.refresh(db_call)

        # Build dynamic variables from request fields
        dynamic_variables = {
            "driver_name": request.driver_name,
            "phone_number": request.phone_number,
            "load_number": request.load_number,
        }

        return retell_service.create_web_call(
            agent_id=request.retell_agent_id,
            retell_llm_dynamic_variables=dynamic_variables,
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to create web call in Retell: {str(e)}"
        ) from e


@router.get("", response_model=list[CallResponse])
def list_calls(session: SessionDep, skip: int = 0, limit: int = 100):
    """List all calls."""
    statement = select(Call).offset(skip).limit(limit)
    calls = session.exec(statement).all()
    return calls


@router.get("/{call_id}", response_model=CallResponse)
def get_call(call_id: int, session: SessionDep):
    """Get a specific call."""
    call = session.get(Call, call_id)
    if not call:
        raise HTTPException(status_code=404, detail="Call not found")
    return call
