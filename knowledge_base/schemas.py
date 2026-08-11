
    
# new

from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class ExtractedDocument(BaseModel):
    source_type: str
    source_name: str
    section: Optional[str] = None
    content: str


class Chunk(BaseModel):
    source_type: str
    source_name: str
    section: Optional[str] = None
    chunk_index: int
    text: str


class EmbeddedChunk(BaseModel):
    source_type: str
    source_name: str
    section: Optional[str] = None
    chunk_index: int
    text: str
    embedding: List[float]


class KnowledgeSource(BaseModel):
    source_type: str
    source_name: str
    chunks: List[EmbeddedChunk]


class KnowledgeBase(BaseModel):
    organization_id: UUID
    sources: List[KnowledgeSource]


class KnowledgeBaseResponse(BaseModel):
    success: bool
    message: str