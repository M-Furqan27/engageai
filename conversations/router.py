from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from conversations.schemas import (
    ConversationCreate,
    ConversationHistoryResponse,
    ConversationMessageCreate,
    ConversationMessageResponse,
    ConversationResponse,
)
from conversations.service import (
    add_assistant_message,
    add_tool_message,
    add_user_message,
    get_conversation_history,
    start_or_get_conversation,
)


router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"],
)


def conversation_to_response(
    conversation,
) -> ConversationResponse:

    return ConversationResponse(
        conversation_id=conversation.id,
        organization_id=conversation.organization_id,
        agent_id=conversation.agent_id,
        lead_id=conversation.lead_id,
        visitor_id=conversation.visitor_id,
        status=conversation.status,
        current_intent=conversation.current_intent,
        handoff_status=conversation.handoff_status,
        assigned_user_id=conversation.assigned_user_id,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at,
    )


def message_to_response(
    message,
) -> ConversationMessageResponse:
    return ConversationMessageResponse(
        message_id=message.id,
        conversation_id=message.conversation_id,
        sender_type=message.sender_type,
        message_text=message.message_text,
        metadata=message.message_metadata,
        created_at=message.created_at,
    )


@router.post(
    "",
    response_model=ConversationResponse,
)
def create_conversation(
    request: ConversationCreate,
    db: Session = Depends(get_db),
):
    try:
        conversation = start_or_get_conversation(
            db=db,
            organization_id=request.organization_id,
            agent_id=request.agent_id,
            lead_id=request.lead_id,
            visitor_id=request.visitor_id,
        )

        return conversation_to_response(conversation)

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error


@router.post(
    "/messages",
    response_model=ConversationMessageResponse,
)
def create_message(
    request: ConversationMessageCreate,
    db: Session = Depends(get_db),
):
    try:
        if request.sender_type == "user":
            message = add_user_message(
                db=db,
                conversation_id=request.conversation_id,
                message_text=request.message_text,
                metadata=request.metadata,
            )

        elif request.sender_type == "assistant":
            message = add_assistant_message(
                db=db,
                conversation_id=request.conversation_id,
                message_text=request.message_text,
                metadata=request.metadata,
            )

        elif request.sender_type == "tool":
            message = add_tool_message(
                db=db,
                conversation_id=request.conversation_id,
                message_text=request.message_text,
                metadata=request.metadata,
            )

        else:
            raise ValueError(
                "System messages cannot be created through this endpoint."
            )

        return message_to_response(message)

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error


@router.get(
    "/{conversation_id}/messages",
    response_model=ConversationHistoryResponse,
)
def get_messages(
    conversation_id: str,
    db: Session = Depends(get_db),
):
    try:
        messages = get_conversation_history(
            db=db,
            conversation_id=conversation_id,
        )

        return ConversationHistoryResponse(
            conversation_id=conversation_id,
            messages=[
                message_to_response(message)
                for message in messages
            ],
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error