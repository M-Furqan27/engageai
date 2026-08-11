from knowledge_base.service import KnowledgeBaseService
from uuid import UUID

class KnowledgeService:


    def __init__(self):

        self.kb_service = KnowledgeBaseService()



    def search_knowledge(
        self,
        organization_id: UUID,
        query: str
    ):


        result = self.kb_service.search(

            organization_id=organization_id,

            query=query

        )


        return result