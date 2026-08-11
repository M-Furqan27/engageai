

# vector database added

from typing import List

from fastapi import UploadFile

# from config import GEMINI_API_KEY
from knowledge_base.chunker import TextChunker
from knowledge_base.embedding import EmbeddingService
from knowledge_base.extractor import Extractor
from knowledge_base.knowledge_builder import KnowledgeBuilder
from knowledge_base.schemas import Chunk
from knowledge_base.vector_store import VectorStore
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)


class KnowledgeBaseService:

    def __init__(self):
        self.extractor = Extractor()
        self.chunker = TextChunker()
        self.embedding = EmbeddingService(api_key=GEMINI_API_KEY)
        self.builder = KnowledgeBuilder()
        self.vector_store = VectorStore()

    async def create(
        self,
        organization_id: int,
        text: str | None,
        urls: List[str],
        pdfs: List[UploadFile],
    ):

        converted_pdfs = []

        for pdf in pdfs:

            if isinstance(pdf, str):

                converted_pdfs.append(
                    UploadFile(
                        filename=os.path.basename(pdf),
                        file=open(
                            pdf,
                            "rb"
                        )
                    )
                )

            else:

                converted_pdfs.append(pdf)

        documents = await self.extractor.extract(
            text=text,
            urls=urls,
            pdfs=converted_pdfs,
        )

        chunks = self.chunker.split(documents)

        embedded_chunks = self.embedding.generate(chunks)

        knowledge_base = self.builder.build(
            organization_id,
            embedded_chunks
        )

        # print("Uploading knowledge to vector store")
        # print(len(knowledge_base.sources))

        self.vector_store.upsert(
            knowledge_base
        )

        return knowledge_base

    def search(
        self,
        organization_id: int,
        query: str
    ):

        query_chunk = Chunk(
            text=query,
            chunk_index=0,
            source_type="query",
            source_name="user_query"
        )

        embedded_chunk = (
            self.embedding
            .generate(
                [
                    query_chunk
                ]
            )[0]
        )

        query_embedding = embedded_chunk.embedding

        results = (
            self.vector_store
            .search(
                organization_id=organization_id,
                query_embedding=query_embedding,
                top_k=5
            )
        )

        return results
