from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.api.deps import SessionDep
from app.models import Call
from app.schemas import CallCreate, CallResponse

router = APIRouter(prefix="/api/calls", tags=["calls"])


@router.post("/trigger", response_model=CallResponse, status_code=201)
def trigger_call(call_data: CallCreate, session: SessionDep):
    """
    Trigger a new call via Retell AI.

    TODO: Implement actual Retell API integration
    """
    # Create call record
    db_call = Call(
        retell_agent_id=call_data.retell_agent_id,
        driver_name=call_data.driver_name,
        phone_number=call_data.phone_number,
        load_number=call_data.load_number,
        status="pending",
    )

    session.add(db_call)
    session.commit()
    session.refresh(db_call)

    # TODO: Call Retell API to actually trigger the call
    # retell_response = retell_service.create_call(...)
    # db_call.retell_call_id = retell_response.call_id
    # db_call.status = "in-progress"
    # session.commit()

    return db_call


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
