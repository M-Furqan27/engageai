from sqlalchemy.orm import Session

from conversations.models import (
    Conversation,
    ConversationMessage,
)
from conversations.repository import (
    get_all_messages,
    get_or_create_conversation,
    get_recent_messages,
    save_message,
    update_conversation_context,
)


def start_or_get_conversation(
    db,
    organization_id,
    agent_id,
    lead_id,
    visitor_id,
) -> Conversation:

    visitor_id = visitor_id.strip()

    if not organization_id:
        raise ValueError("organization_id is required.")

    if not agent_id:
        raise ValueError("agent_id is required.")

    if not visitor_id:
        raise ValueError("visitor_id is required.")


    return get_or_create_conversation(
        db=db,
        organization_id=organization_id,
        agent_id=agent_id,
        lead_id=lead_id,
        visitor_id=visitor_id,
    )

def add_user_message(
    db: Session,
    conversation_id: str,
    message_text: str,
    metadata: dict | None = None,
) -> ConversationMessage:
    message_text = message_text.strip()

    if not message_text:
        raise ValueError("User message cannot be empty.")

    return save_message(
        db=db,
        conversation_id=conversation_id,
        sender_type="user",
        message_text=message_text,
        metadata=metadata,
    )


def add_assistant_message(
    db: Session,
    conversation_id: str,
    message_text: str,
    metadata: dict | None = None,
) -> ConversationMessage:
    message_text = message_text.strip()

    if not message_text:
        raise ValueError("Assistant message cannot be empty.")

    return save_message(
        db=db,
        conversation_id=conversation_id,
        sender_type="assistant",
        message_text=message_text,
        metadata=metadata,
    )


def add_tool_message(
    db: Session,
    conversation_id: str,
    message_text: str,
    metadata: dict | None = None,
) -> ConversationMessage:
    message_text = message_text.strip()

    if not message_text:
        raise ValueError("Tool message cannot be empty.")

    return save_message(
        db=db,
        conversation_id=conversation_id,
        sender_type="tool",
        message_text=message_text,
        metadata=metadata,
    )


def get_conversation_history(
    db: Session,
    conversation_id: str,
) -> list[ConversationMessage]:
    return get_all_messages(
        db=db,
        conversation_id=conversation_id,
    )


def get_recent_conversation_messages(
    db: Session,
    conversation_id: str,
    limit: int = 8,
) -> list[ConversationMessage]:
    if limit < 1:
        raise ValueError("Message limit must be at least 1.")

    return get_recent_messages(
        db=db,
        conversation_id=conversation_id,
        limit=limit,
    )


def build_history_for_agent(
    db: Session,
    conversation_id: str,
    limit: int = 8,
) -> list[dict[str, str]]:
    messages = get_recent_conversation_messages(
        db=db,
        conversation_id=conversation_id,
        limit=limit,
    )

    history: list[dict[str, str]] = []

    for message in messages:
        role = message.sender_type

        if role not in {
            "user",
            "assistant",
            "system",
            "tool",
        }:
            continue

        history.append(
            {
                "role": role,
                "content": message.message_text,
            }
        )

    return history


def update_agent_context(
    db: Session,
    conversation: Conversation,
    current_intent: str | None = None,
    handoff_required: bool | None = None,
    assigned_user_id: str | None = None,
) -> Conversation:
    handoff_status = None

    if handoff_required is True:
        handoff_status = "required"

    elif handoff_required is False:
        handoff_status = "not_required"

    return update_conversation_context(
        db=db,
        conversation=conversation,
        current_intent=current_intent,
        handoff_status=handoff_status,
        assigned_user_id=assigned_user_id,
    )