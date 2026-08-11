from knowledge_base.service import KnowledgeBaseService


class KnowledgeService:


    def __init__(self):

        self.kb_service = KnowledgeBaseService()



    def search_knowledge(
        self,
        organization_id: int,
        query: str
    ):


        result = self.kb_service.search(

            organization_id=organization_id,

            query=query

        )


        return result