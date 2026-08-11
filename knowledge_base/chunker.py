
from typing import List

from langchain_text_splitters import RecursiveCharacterTextSplitter

from knowledge_base.schemas import (
    Chunk,
    ExtractedDocument,
)


class TextChunker:

    def __init__(
        self,
        chunk_size: int = 1500,
        chunk_overlap: int = 200,
    ):

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    def split(
        self,
        documents: List[ExtractedDocument],
    ) -> List[Chunk]:

        chunks: List[Chunk] = []

        for document in documents:

            document_chunks = self.splitter.split_text(
                document.content
            )

            for index, chunk in enumerate(document_chunks):

                chunks.append(
                    Chunk(
                        source_type=document.source_type,
                        source_name=document.source_name,
                        section=document.section,
                        chunk_index=index + 1,
                        text=chunk,
                    )
                )

        return chunks