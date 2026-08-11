from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field


SenderType = Literal[
    "user",
    "assistant",
    "system",
    "tool",
]


class ConversationCreate(BaseModel):

    organization_id: int = Field(
        ...,
        gt=0,
    )

    agent_id: int = Field(
        ...,
        gt=0,
    )

    lead_id: int | None = Field(
        default=None,
        gt=0,
    )

    visitor_id: str = Field(
        ...,
        min_length=1,
    )


class ConversationResponse(BaseModel):

    conversation_id: int

    organization_id: int

    agent_id: int

    lead_id: int | None = None

    visitor_id: str

    status: str = "active"

    current_intent: str | None = None

    handoff_status: str | None = None

    assigned_user_id: str | None = None

    created_at: datetime

    updated_at: datetime


class ConversationMessageCreate(BaseModel):

    conversation_id: int = Field(
        ...,
        gt=0,
    )

    sender_type: SenderType

    message_text: str = Field(
        ...,
        min_length=1,
    )

    metadata: dict[str, Any] | None = None


class ConversationMessageResponse(BaseModel):

    message_id: int

    conversation_id: int

    sender_type: SenderType

    message_text: str

    metadata: dict[str, Any] | None = None

    created_at: datetime


class ConversationHistoryResponse(BaseModel):
    conversation_id: int
    messages: list[ConversationMessageResponse]


class AgentConversationRequest(BaseModel):

    organization_id: int = Field(
        ...,
        gt=0,
    )

    agent_id: int = Field(
        ...,
        gt=0,
    )

    lead_id: int | None = Field(
        default=None,
        gt=0,
    )

    visitor_id: str = Field(
        ...,
        min_length=1,
    )

    conversation_id: int | None = Field(
        default=None,
        gt=0,
    )

    message: str = Field(
        ...,
        min_length=1,
    )