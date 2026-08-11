from sqlalchemy import select
from sqlalchemy.orm import Session

from conversations.models import (
    Conversation,
    ConversationMessage,
)


def create_conversation(
    db: Session,
    organization_id: int,
    agent_id: int,
    lead_id: int | None,
    visitor_id: str,
) -> Conversation:
    conversation = Conversation(
    organization_id=organization_id,
    agent_id=agent_id,
    lead_id=lead_id,
    visitor_id=visitor_id,
    status="active",
)

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return conversation


def get_conversation(
    db: Session,
    conversation_id: int,
) -> Conversation | None:
    statement = select(Conversation).where(
        Conversation.id == conversation_id
    )

    return db.scalar(statement)


def get_or_create_conversation(
    db,
    organization_id,
    agent_id,
    lead_id,
    visitor_id,
):

    conversation = (
        db.query(Conversation)
        .filter(
            Conversation.organization_id == organization_id,
            Conversation.agent_id == agent_id,
            Conversation.visitor_id == visitor_id,
        )
        .first()
    )


    if conversation:
        return conversation


    conversation = Conversation(
        organization_id=organization_id,
        agent_id=agent_id,
        lead_id=lead_id,
        visitor_id=visitor_id,
        status="active",
    )


    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return conversation


def save_message(
    db: Session,
    conversation_id: int,
    sender_type: str,
    message_text: str,
    metadata: dict | None = None,
) -> ConversationMessage:
    conversation = get_conversation(
        db=db,
        conversation_id=conversation_id,
    )

    if not conversation:
        raise ValueError("Conversation not found.")

    message = ConversationMessage(
        conversation_id=conversation_id,
        sender_type=sender_type,
        message_text=message_text,
        message_metadata=metadata,
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return message


def get_recent_messages(
    db: Session,
    conversation_id: int,
    limit: int = 8,
) -> list[ConversationMessage]:
    statement = (
        select(ConversationMessage)
        .where(
            ConversationMessage.conversation_id
            == conversation_id
        )
        .order_by(
            ConversationMessage.created_at.desc()
        )
        .limit(limit)
    )

    messages = list(db.scalars(statement).all())

    messages.reverse()

    return messages


def get_all_messages(
    db: Session,
    conversation_id: int,
) -> list[ConversationMessage]:
    statement = (
        select(ConversationMessage)
        .where(
            ConversationMessage.conversation_id
            == conversation_id
        )
        .order_by(
            ConversationMessage.created_at.asc()
        )
    )

    return list(db.scalars(statement).all())


def update_conversation_context(
    db: Session,
    conversation: Conversation,
    current_intent: str | None = None,
    handoff_status: str | None = None,
    assigned_user_id: str | None = None,
) -> Conversation:
    if current_intent is not None:
        conversation.current_intent = current_intent

    if handoff_status is not None:
        conversation.handoff_status = handoff_status

    if assigned_user_id is not None:
        conversation.assigned_user_id = assigned_user_id

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return conversation