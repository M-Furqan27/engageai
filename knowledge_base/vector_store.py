
# new


# import chromadb

import os

from knowledge_base.schemas import KnowledgeBase

from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.models import VectorizedQuery
import uuid


class VectorStore:

    def __init__(self):

        self.client = SearchClient(

            endpoint=os.getenv(
                "AZURE_SEARCH_ENDPOINT"
            ),

            index_name=os.getenv(
                "AZURE_SEARCH_INDEX_NAME"
            ),

            credential=AzureKeyCredential(
                os.getenv(
                    "AZURE_SEARCH_KEY"
                )
            )
        )

    def upsert(
        self,
        knowledge_base: KnowledgeBase
    ) -> None:

        documents = []

        for source in knowledge_base.sources:

            for chunk in source.chunks:

                documents.append({

                    # "id":
                    # (
                    #     f"{source.source_type}_"
                    #     f"{source.source_name.replace(' ', '_').replace('.', '_')}_"
                    #     f"{chunk.chunk_index}"
                    # )
                    "id": str(uuid.uuid4()),

                    "organization_id":
                    str(
                        knowledge_base.organization_id
                    ),


                    "content":
                    chunk.text,


                    "content_vector":
                    chunk.embedding,


                    "source_type":
                    chunk.source_type,


                    "source_name":
                    source.source_name

                })

        if documents:

            # print("DOCUMENTS TO UPLOAD:")
            # print(len(documents))

            self.client.upload_documents(
                documents
            )

    def search(
        self,
        organization_id: int,
        query_embedding: list,
        top_k: int = 5
    ):

        vector_query = VectorizedQuery(
            vector=query_embedding,
            k_nearest_neighbors=top_k,
            fields="content_vector"
        )

        results = self.client.search(

            vector_queries=[
                vector_query
            ],

            filter=f"organization_id eq '{organization_id}'",

            select=[
                "content",
                "source_name",
                "source_type"
            ]
        )

        return list(results)
