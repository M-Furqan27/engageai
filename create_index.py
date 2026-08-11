import os

from dotenv import load_dotenv

from azure.core.credentials import AzureKeyCredential

from azure.search.documents.indexes import SearchIndexClient

from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchField,
    SearchFieldDataType,
    VectorSearch,
    HnswAlgorithmConfiguration,
    VectorSearchProfile,
)


load_dotenv()


AZURE_SEARCH_ENDPOINT = os.getenv(
    "AZURE_SEARCH_ENDPOINT"
)

AZURE_SEARCH_KEY = os.getenv(
    "AZURE_SEARCH_KEY"
)

INDEX_NAME = os.getenv(
    "AZURE_SEARCH_INDEX_NAME",
    "knowledge-index"
)


if not AZURE_SEARCH_ENDPOINT:
    raise ValueError(
        "AZURE_SEARCH_ENDPOINT missing in .env"
    )


if not AZURE_SEARCH_KEY:
    raise ValueError(
        "AZURE_SEARCH_KEY missing in .env"
    )


client = SearchIndexClient(

    endpoint=AZURE_SEARCH_ENDPOINT,

    credential=AzureKeyCredential(
        AZURE_SEARCH_KEY
    )

)


fields = [

    # Unique document id
    SimpleField(
        name="id",

        type=SearchFieldDataType.String,

        key=True
    ),


    # Multi tenant filtering
    SimpleField(
        name="organization_id",

        type=SearchFieldDataType.String,

        filterable=True
    ),


    # Chunk text
    SearchField(
        name="content",

        type=SearchFieldDataType.String,

        searchable=True
    ),


    # Embedding vector
    SearchField(

        name="content_vector",

        type=SearchFieldDataType.Collection(
            SearchFieldDataType.Single
        ),

        searchable=True,

        vector_search_dimensions=3072,

        vector_search_profile_name="vector-profile"
    ),


    # Metadata
    SimpleField(

        name="source_name",

        type=SearchFieldDataType.String,

        filterable=True
    ),


    SimpleField(

        name="source_type",

        type=SearchFieldDataType.String,

        filterable=True
    )

]


vector_search = VectorSearch(

    algorithms=[

        HnswAlgorithmConfiguration(

            name="hnsw-config"

        )

    ],


    profiles=[

        VectorSearchProfile(

            name="vector-profile",

            algorithm_configuration_name="hnsw-config"

        )

    ]

)



index = SearchIndex(

    name=INDEX_NAME,

    fields=fields,

    vector_search=vector_search

)



result = client.create_or_update_index(
    index
)


print("Index created successfully:")

print(result.name)