from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
    JSON,
    String,
    Text,
)

from sqlalchemy.orm import relationship

from sqlalchemy.dialects.postgresql import UUID

from database.database import Base

import uuid


def utc_now():
    return datetime.now(timezone.utc)



class Conversation(Base):

    __tablename__ = "conversations"


    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )


    organization_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "organizations.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )


    agent_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "agents.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )


    azure_conversation_id = Column(
        String,
        nullable=True
    )


    visitor_id = Column(
        String(100),
        nullable=False,
        index=True
    )


    lead_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "leads.id",
            ondelete="SET NULL"
        ),
        nullable=True
    )


    status = Column(
        String(30),
        default="active"
    )


    current_intent = Column(
        String(100),
        nullable=True
    )


    handoff_status = Column(
        String(30),
        nullable=True
    )


    assigned_user_id = Column(
        String(100),
        nullable=True
    )


    created_at = Column(
        DateTime(timezone=True),
        default=utc_now
    )


    updated_at = Column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now
    )


    messages = relationship(
        "ConversationMessage",
        back_populates="conversation",
        cascade="all, delete-orphan"
    )



class ConversationMessage(Base):

    __tablename__ = "conversation_messages"


    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )


    conversation_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "conversations.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )


    sender_type = Column(
        String(20),
        nullable=False
    )


    message_text = Column(
        Text,
        nullable=False
    )


    message_metadata = Column(
        "metadata",
        JSON,
        nullable=True
    )


    created_at = Column(
        DateTime(timezone=True),
        default=utc_now
    )


    conversation = relationship(
        "Conversation",
        back_populates="messages"
    )