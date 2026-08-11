import os
from dotenv import load_dotenv

from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential


load_dotenv()


client = SearchClient(
    endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
    index_name="knowledge-index",
    credential=AzureKeyCredential(
        os.getenv("AZURE_SEARCH_KEY")
    )
)


# delete all documents for organization 1
results = client.search(
    search_text="*",
    filter="organization_id eq '2'"
)


documents = []

for doc in results:
    documents.append(
        {
            "id": doc["id"]
        }
    )


if documents:
    client.delete_documents(documents)

print(
    f"Deleted {len(documents)} documents"
)