from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    TIMESTAMP
)

from sqlalchemy.orm import relationship

from datetime import datetime


from database.database import Base

from conversations.models import Conversation, ConversationMessage



class Organization(Base):

    __tablename__ = "organizations"


    id = Column(
        Integer,
        primary_key=True
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


    id = Column(
        Integer,
        primary_key=True
    )


    organization_id = Column(
        Integer,
        ForeignKey(
            "organizations.id"
        )
    )


    name = Column(
        String(255),
        nullable=False
    )


    email = Column(
        String(255),
        unique=True
    )


    created_at = Column(
        TIMESTAMP,
        default=datetime.utcnow
    )



    organization = relationship(
        "Organization",
        back_populates="representatives"
    )


    services = relationship(
        "Service",
        back_populates="representative"
    )





class Service(Base):

    __tablename__ = "services"


    id = Column(
        Integer,
        primary_key=True
    )


    representative_id = Column(
        Integer,
        ForeignKey(
            "representatives.id"
        )
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



    representative = relationship(
        "Representative",
        back_populates="services"
    )
    
class Agent(Base):

    __tablename__ = "agents"


    id = Column(
        Integer,
        primary_key=True
    )


    organization_id = Column(
        Integer,
        ForeignKey("organizations.id")
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
        Integer,
        primary_key=True,
        autoincrement=True
    )


    organization_id = Column(
        Integer,
        ForeignKey(
            "organizations.id"
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