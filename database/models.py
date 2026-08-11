from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    TIMESTAMP,
    Boolean,
    DateTime,
)

from sqlalchemy.orm import relationship

from datetime import datetime

from database.database import Base

from sqlalchemy.dialects.postgresql import UUID

import uuid


class Organization(Base):

    __tablename__ = "organizations"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    name = Column(
        String(255),
        nullable=False
    )

    description = Column(
        Text
    )

    created_at = Column(
        TIMESTAMP,
        default=datetime.utcnow
    )


    representatives = relationship(
        "Representative",
        back_populates="organization"
    )



class Representative(Base):

    __tablename__ = "representatives"


    representative_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )


    organization_id = Column(
        UUID(as_uuid=True),
        nullable=False
    )


    representative_name = Column(
        String(150),
        nullable=False
    )


    service = Column(
        String(150),
        nullable=False
    )


    service_description = Column(
        Text,
        nullable=False
    )


    company_email = Column(
        String(255),
        nullable=False
    )


    invitation_status = Column(
        String(30),
        default="Pending"
    )


    calendar_connected = Column(
        Boolean,
        default=False
    )


    status = Column(
        String(30),
        default="Active"
    )


    created_at = Column(
        DateTime(timezone=True),
        default=datetime.utcnow
    )


    updated_at = Column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


    organization = relationship(
        "Organization",
        back_populates="representatives"
    )



class Agent(Base):

    __tablename__ = "agents"


    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )


    organization_id = Column(
        UUID(as_uuid=True),
        nullable=False
    )


    azure_agent_name = Column(
        String(255)
    )


    azure_agent_version = Column(
        String(100)
    )


    system_prompt = Column(
        Text
    )


    created_at = Column(
        TIMESTAMP,
        default=datetime.utcnow
    )



class Lead(Base):

    __tablename__ = "leads"


    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )


    organization_id = Column(
        UUID(as_uuid=True),
        nullable=False
    )


    name = Column(
        String(255),
        nullable=True
    )


    email = Column(
        String(255),
        nullable=True
    )


    phone = Column(
        String(50),
        nullable=True
    )


    created_at = Column(
        TIMESTAMP,
        default=datetime.utcnow
    )