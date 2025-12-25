from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.api.deps import CurrentUserDep, RetellServiceDep, SessionDep
from app.models import Call, CallResult
from app.schemas import CallCreate, CallResponse

router = APIRouter(prefix="/api/calls", tags=["calls"])


@router.post("webcall/", status_code=201)
def create_web_call(
    request: CallCreate,
    retell_service: RetellServiceDep,
    session: SessionDep,
    user: CurrentUserDep,
):
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
        # Build dynamic variables from request fields
        dynamic_variables = {
            "driver_name": request.driver_name,
            "phone_number": request.phone_number,
            "load_number": request.load_number,
        }

        retell_call = retell_service.create_web_call(
            agent_id=request.agent_id,
            retell_llm_dynamic_variables=dynamic_variables,
        )

        db_call = Call(
            id=retell_call.call_id,
            agent_id=request.agent_id,
            driver_name=request.driver_name,
            phone_number=request.phone_number,
            load_number=request.load_number,
            status="pending",
        )

        session.add(db_call)
        session.commit()

        return retell_call
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to create web call in Retell: {str(e)}"
        ) from e


@router.get("", response_model=list[CallResponse])
def list_calls(session: SessionDep, user: CurrentUserDep, skip: int = 0, limit: int = 100):
    """List all calls."""
    statement = select(Call).offset(skip).limit(limit)
    calls = session.exec(statement).all()
    return calls


@router.get("/{call_id}", response_model=CallResponse)
def get_call(call_id: str, session: SessionDep, user: CurrentUserDep):
    """
    Get a specific call with its transcript and structured data.

    Fetches the call details along with the associated call result
    (transcript and structured data) if available.
    """
    call = session.get(Call, call_id)
    if not call:
        raise HTTPException(status_code=404, detail="Call not found")

    # Fetch the associated call result
    call_result = session.exec(select(CallResult).where(CallResult.call_id == call_id)).first()

    # Build response with call data and optionally call result data
    response_data = {
        "id": call.id,
        "agent_id": call.agent_id,
        "driver_name": call.driver_name,
        "phone_number": call.phone_number,
        "load_number": call.load_number,
        "status": call.status,
        "created_at": call.created_at,
        "updated_at": call.updated_at,
        "transcript": call_result.transcript if call_result else None,
        "structured_data": call_result.structured_data if call_result else None,
    }

    return response_data
