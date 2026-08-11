from fastapi import APIRouter, HTTPException

from widget.schemas import WidgetChatRequest
from widget.service import process_widget_message


router = APIRouter(
    prefix="/widget",
    tags=["Widget"]
)


@router.post("/chat")
def widget_chat(payload: WidgetChatRequest):

    try:

        response = process_widget_message(
            organization_id=payload.organization_id,
            agent_id=payload.agent_id,
            visitor_id=payload.visitor_id,
            message=payload.message
        )

        return response

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )