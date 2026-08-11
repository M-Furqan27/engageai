from agents.main_agent import MainAgent
from knowledge_base.service import KnowledgeBaseService
from uuid import UUID


class PipelineService:

    def __init__(self):

        self.agent_service = MainAgent()
        self.knowledge_service = KnowledgeBaseService()


    async def setup(
        self,
        organization_id: UUID,
        text: str | None = None,
        urls: list[str] = [],
        pdfs: list = []
    ):

        # Step 1: Create Agent

        agent = (
            self.agent_service
            .create_agent(
                organization_id
            )
        )


        # Step 2: Create Knowledge Base

        knowledge = await (
            self.knowledge_service
            .create(
                organization_id=organization_id,
                text=text,
                urls=urls,
                pdfs=pdfs
            )
        )


        return {
            "agent": agent,
            "knowledge": knowledge
        }