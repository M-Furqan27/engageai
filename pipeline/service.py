from agents.main_agent import MainAgent
from knowledge_base.service import KnowledgeBaseService

from pipeline.schemas import PipelineSetupRequest


class PipelineService:

    def __init__(self):

        self.agent_service = MainAgent()
        self.knowledge_service = KnowledgeBaseService()

    async def setup(
        self,
        request: PipelineSetupRequest
    ):

        # Step 1: Create Agent

        agent = (
            self.agent_service
            .create_agent(
                request.organization_id
            )
        )

        # Step 2: Create Knowledge Base

        knowledge = await (
            self.knowledge_service
            .create(
                organization_id=request.organization_id,
                text=request.text,
                urls=[],
                pdfs=request.documents
            )
        )

        # print("KNOWLEDGE CREATED")
        # print(knowledge)

        return {
            "agent": agent,
            "knowledge": knowledge
        }
