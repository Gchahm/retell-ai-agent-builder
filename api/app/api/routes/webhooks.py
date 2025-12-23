import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Literal

from fastapi import APIRouter, BackgroundTasks, HTTPException, Request
from pydantic import BaseModel
from sqlmodel import select

from app.api.deps import SessionDep
from app.models import Call, CallResult
from app.services.post_processing import PostProcessingService

router = APIRouter(prefix="/api/webhooks", tags=["webhooks"])
logger = logging.getLogger(__name__)

# Directory for storing webhook payloads
WEBHOOK_LOGS_DIR = Path("webhook_logs")
WEBHOOK_LOGS_DIR.mkdir(exist_ok=True)


class WebhookPayload(BaseModel):
    """Schema for Retell webhook payload."""

    event: Literal["call_started", "call_ended", "call_analyzed"]
    call: dict  # Call data structure from Retell


@router.post("/retell", status_code=204)
async def retell_webhook(request: Request, background_tasks: BackgroundTasks, session: SessionDep):
    """
    Receive webhooks from Retell AI.

    Events:
    - call_started: Call has begun
    - call_ended: Call has completed/failed
    - call_analyzed: Call analysis is complete (includes transcript)

    Note: Must respond within 10 seconds. Processing happens in background.
    """
    # TODO: Implement webhook signature verification
    # signature = request.headers.get("x-retell-signature")
    # if not verify_signature(await request.body(), signature):
    #     raise HTTPException(status_code=401, detail="Invalid signature")

    try:
        payload = WebhookPayload.model_validate(await request.json())
    except Exception as e:
        logger.error(f"Invalid webhook payload: {e}")
        raise HTTPException(status_code=400, detail="Invalid payload") from e

    # Process in background to respond quickly (10s timeout)
    background_tasks.add_task(process_webhook, payload, session)

    # Return 204 No Content (successful acknowledgment)
    return None


def process_webhook(payload: WebhookPayload, session: SessionDep):
    """
    Process webhook event in background.

    Updates the database based on the event type:
    - call_started: Update status to "in-progress"
    - call_ended: Update status to "completed" or "failed"
    - call_analyzed: Store transcript and structured data
    """
    event = payload.event
    call_data = payload.call

    # Get the Retell call ID
    retell_call_id = call_data.get("call_id")
    if not retell_call_id:
        logger.error(f"No call_id in webhook payload for event: {event}")
        return

    # Save payload to JSON file for debugging/inspection
    # TODO: REMOVE - this is a temporary dev log remove later
    try:
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{retell_call_id}_{event}.json"
        filepath = WEBHOOK_LOGS_DIR / filename

        with open(filepath, "w") as f:
            json.dump(payload.model_dump(), f, indent=2, default=str)

        logger.info(f"Saved webhook payload to {filepath}")
    except Exception as e:
        logger.error(f"Failed to save webhook payload: {e}")

    # Find our Call record by retell_call_id
    statement = select(Call).where(Call.retell_call_id == retell_call_id)
    db_call = session.exec(statement).first()

    if not db_call:
        logger.warning(f"Call not found for retell_call_id: {retell_call_id}")
        return

    try:
        if event == "call_started":
            db_call.status = "in-progress"
            session.add(db_call)
            session.commit()
            logger.info(f"Call {retell_call_id} started")

        elif event == "call_ended":
            # Determine if call was successful or failed
            call_status = call_data.get("call_status", "unknown")
            if call_status == "ended":
                db_call.status = "completed"
            else:
                db_call.status = "failed"

            session.add(db_call)
            session.commit()
            logger.info(f"Call {retell_call_id} ended with status: {call_status}")

        elif event == "call_analyzed":
            # Store transcript and create CallResult
            transcript = call_data.get("transcript", "")

            # Check if CallResult already exists
            existing_result = session.exec(
                select(CallResult).where(CallResult.call_id == db_call.id)
            ).first()

            if not existing_result:
                call_result = CallResult(
                    call_id=db_call.id,
                    transcript=transcript,
                    structured_data={},  # TODO: Implement LLM post-processing
                )
                session.add(call_result)
                session.commit()
                logger.info(f"Call {retell_call_id} analyzed, transcript stored")

                # TODO: Trigger LLM post-processing to extract structured data
                # structured_data = extract_structured_data(transcript, db_call.retell_agent_id)
                # call_result.structured_data = structured_data
                # session.commit()

    except Exception as e:
        logger.error(f"Error processing webhook for call {retell_call_id}: {e}")
        session.rollback()
