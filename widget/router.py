from fastapi import APIRouter
from pydantic import BaseModel

from agents.runtime import AgentRuntime


router = APIRouter()


class WidgetChatRequest(BaseModel):
    organization_id: int
    agent_id: int
    visitor_id: str
    message: str



@router.post("/widget/chat")
def widget_chat(
    request: WidgetChatRequest
):

    runtime = AgentRuntime()

    response = runtime.chat(
    organization_id=request.organization_id,
    agent_id=request.agent_id,
    visitor_id=request.visitor_id,
    message=request.message,
    lead_id=None
)
    return {
        "response": response
    }