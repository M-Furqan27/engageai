from fastapi import FastAPI

from database.database import Base, engine

# Register existing models
from database.models import (
    Organization,
    Representative,
    Agent,
    Lead
)

from pipeline.router import router as pipeline_router

from fastapi.middleware.cors import CORSMiddleware


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="AI Agent Platform"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pipeline setup endpoint
app.include_router(
    pipeline_router
)


@app.get("/")
def root():

    return {
        "status": "running"
    }