from fastapi import APIRouter, BackgroundTasks, Request

router = APIRouter(prefix="/api/webhooks", tags=["webhooks"])


@router.post("/retell")
async def retell_webhook(request: Request, background_tasks: BackgroundTasks):
    """
    Receive webhooks from Retell AI.

    TODO: Implement webhook signature verification
    TODO: Process webhook events
    TODO: Extract and store transcript
    TODO: Trigger post-processing
    """
    _payload = await request.json()

    # TODO: Verify webhook signature
    # verify_retell_signature(request.headers, _payload)

    # TODO: Process different webhook events
    # - call.started
    # - call.ended
    # - call.analyzed

    # Acknowledge immediately (webhooks have 10s timeout)
    return {"status": "received"}


def process_webhook_background(payload: dict):
    """
    Process webhook in background.

    TODO: Implement background processing
    TODO: Update call status
    TODO: Store transcript
    TODO: Trigger LLM post-processing
    """
    pass
