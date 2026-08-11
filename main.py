from fastapi import FastAPI

from database.database import Base, engine

# Register existing models
from database.models import (
    Organization,
    Representative,
    # Service,
    Agent
)

# Register conversation models
from conversations.models import (
    Conversation,
    ConversationMessage
)


from pipeline.router import router as pipeline_router
from conversations.router import router as conversation_router
from widget.router import router as widget_router
from fastapi.middleware.cors import CORSMiddleware




Base.metadata.create_all(bind=engine)


app = FastAPI(title="AI Agent Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(pipeline_router)


app.include_router(conversation_router)

app.include_router(widget_router)

@app.get("/")
def root():

    return {
        "status": "running"
    }