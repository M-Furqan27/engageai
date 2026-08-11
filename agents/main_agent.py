import os

from dotenv import load_dotenv

from azure.ai.projects import AIProjectClient

from azure.ai.projects.models import PromptAgentDefinition

from azure.identity import DefaultAzureCredential


from database.database import get_session

from services.organization_service import OrganizationService

from services.agent_service import AgentService

from agents.prompt_builder import PromptBuilder

from azure.ai.projects.models import FunctionTool

from services.knowledge_service import KnowledgeService

from tools.calendar_tools import (
    get_available_slots,
    create_calendar_event
)



class MainAgent:


    def __init__(self):

        load_dotenv()


        self.project_endpoint = os.getenv(
            "PROJECT_ENDPOINT"
        )


        self.model_deployment = os.getenv(
            "MODEL_DEPLOYMENT_NAME"
        )

        self.agent_service = AgentService()
        
        self.knowledge_service = KnowledgeService()

        self.organization_service = OrganizationService()

        self.prompt_builder = PromptBuilder()



    def create_agent(
    self,
    organization_id
    ):

        db = get_session()

        try:

            # existing_agent = (
            #     self.agent_service
            #     .get_agent(
            #         db,
            #         organization_id
            #     )
            # )


            # if existing_agent:

            #     # print("Existing agent found")

            #     return existing_agent



            agent_context = (
                self.organization_service
                .get_agent_context(
                    db,
                    organization_id
                )
            )


            instructions = (
                self.prompt_builder
                .build_prompt(
                    agent_context
                )
            )


            print("\nGenerated Agent Instructions:\n")
            print(instructions)
            
            knowledge_search_tool = FunctionTool(

                name="knowledge_search",

                description=
                "Search the organization's knowledge base to find relevant information for customer questions.",


                parameters={

                    "type": "object",

                    "properties": {

                        "query": {

                            "type": "string",

                            "description":
                            "The customer's question to search in the knowledge base."

                        }

                    },


                    "required": [
                        "query"
                    ],


                    "additionalProperties": False

                },

                strict=True

            )
            
            get_available_slots_tool = FunctionTool(

                name="get_available_slots",

                    description=(
                        "Check a representative's Google Calendar for free meeting slots "
                        "on a customer-proposed date. The customer does not need to provide "
                        "an exact time. Return up to 3 available slots at a time. "
                        "If the customer asks for more slots, call this tool again using "
                        "the next_offset returned by the previous call."
                    ),

                    parameters={

                        "type": "object",

                        "properties": {

                            "organization_id": {
                                "type": "string",
                                "description": "The organization ID."
                            },

                            "representative_id": {
                                "type": "string",
                                "description": "The UUID of the representative whose calendar should be checked."
                            },

                            "proposed_date": {
                                "type": "string",
                                "description": "The date proposed by the customer in YYYY-MM-DD format."
                            },

                            "duration_minutes": {
                                "type": "integer",
                                "description": "Required meeting duration in minutes."
                            },

                            "offset": {
                                "type": "integer",
                                "description": (
                                    "Pagination offset. Use 0 for the first three slots. "
                                    "When the customer asks for more slots, use the "
                                    "next_offset returned by the previous call."
                                )
                            },

                            "limit": {
                                "type": "integer",
                                "description": "Number of slots to return. Always use 3."
                            }

                        },

                        "required": [
                            "organization_id",
                            "representative_id",
                            "proposed_date",
                            "duration_minutes",
                            "offset",
                            "limit"
                        ],

                        "additionalProperties": False

                    },

                    strict=True
                )


            create_calendar_event_tool = FunctionTool(

                    name="create_calendar_event",

                    description=
                    "Create a calendar event after customer selects an available slot.",


                    parameters={

                        "type": "object",

                        "properties": {

                            "representative_id": {
                                "type": "string"
                            },

                            "customer_name": {
                                "type": "string"
                            },

                            "customer_email": {
                                "type": "string"
                            },

                            "service": {
                                "type": "string"
                            },

                            "slot_start": {
                                "type": "string"
                            },

                            "slot_end": {
                                "type": "string"
                            }

                        },


                        "required": [

                            "representative_id",
                            "customer_name",
                            "customer_email",
                            "service",
                            "slot_start",
                            "slot_end"

                        ],

                        "additionalProperties": False

                    },

                    strict=True
                )

            with DefaultAzureCredential() as credential:


                with AIProjectClient(
                    endpoint=self.project_endpoint,
                    credential=credential

                ) as project_client:


                    agent = (
                        project_client
                        .agents
                        .create_version(

                            agent_name=
                            f"organization-{organization_id}-agent",


                            definition=
                            PromptAgentDefinition(

                                model=
                                self.model_deployment,


                                instructions=
                                instructions,


                                tools=[

                                    knowledge_search_tool,

                                    get_available_slots_tool,

                                    create_calendar_event_tool

                                ]

                            )
                        )
                    )


            self.agent_service.save_agent(
                db,
                organization_id,
                agent,
                instructions
            )


            return agent



        finally:

            db.close()