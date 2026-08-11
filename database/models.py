from sqlalchemy import (
    Column,
    String,
    Text,
    TIMESTAMP,
    Boolean,
    DateTime,
    ForeignKey,
)

from sqlalchemy.orm import relationship

from datetime import datetime

from database.database import Base

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy import ForeignKey

import uuid


# =========================
# Organization
# =========================

class Organization(Base):

    __tablename__ = "organizations"

    organization_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    organization_name = Column(
        String(150),
        nullable=False
    )

    business_type = Column(
        String(100),
        nullable=True
    )

    website = Column(
        String(255),
        nullable=True
    )

    business_email = Column(
        String(255),
        nullable=True
    )

    business_phone = Column(
        String(20),
        nullable=True
    )

    country = Column(
        String(100),
        nullable=True
    )

    address = Column(
        Text,
        nullable=True
    )

    description = Column(
        Text,
        nullable=True
    )

    logo_url = Column(
        String(255),
        nullable=True
    )

    onboarding_completed = Column(
        Boolean,
        default=False
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


    representatives = relationship(
        "Representative",
        back_populates="organization",
        cascade="all, delete-orphan"
    )



# =========================
# Representative
# =========================

class Representative(Base):

    __tablename__ = "representatives"


    representative_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )


    organization_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "organizations.organization_id",
            ondelete="CASCADE"
        ),
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



# =========================
# Agent
# =========================

class Agent(Base):

    __tablename__ = "agents"


    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )


    organization_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "organizations.organization_id",
            ondelete="CASCADE"
        ),
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



# =========================
# Lead
# =========================

class Lead(Base):

    __tablename__ = "leads"


    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )


    organization_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "organizations.organization_id",
            ondelete="CASCADE"
        ),
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