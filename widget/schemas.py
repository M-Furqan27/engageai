from pydantic import BaseModel


class WidgetChatRequest(BaseModel):
    organization_id: str
    agent_id: str
    visitor_id: str
    message: str