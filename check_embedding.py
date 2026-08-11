from dotenv import load_dotenv
import os

from knowledge_base.embedding import EmbeddingService
from knowledge_base.schemas import Chunk


load_dotenv()


GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)


embedding = EmbeddingService(
    api_key=GEMINI_API_KEY
)


chunk = Chunk(
    text="test embedding",
    chunk_index=0,
    source_type="test",
    source_name="test"
)


result = embedding.generate(
    [chunk]
)[0]


print(
    "Embedding dimension:",
    len(result.embedding)
)