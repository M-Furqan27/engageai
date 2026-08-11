import os
import json

from dotenv import load_dotenv

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

from openai.types.responses.response_input_param import FunctionCallOutput

from database.database import get_session

from services.agent_service import AgentService
from services.knowledge_service import KnowledgeService

from tools.calendar_tools import (
    get_available_slots,
    create_calendar_event
)


class AgentRuntime:


    def __init__(self):

        load_dotenv()

        self.project_endpoint = os.getenv(
            "PROJECT_ENDPOINT"
        )

        self.agent_service = AgentService()

        self.knowledge_service = KnowledgeService()



    def chat_from_widget(
        self,
        organization_id,
        agent_id,
        visitor_id,
        message,
        lead_id=None,
    ):

        db = get_session()

        try:

            agent_record = (
                self.agent_service
                .get_agent(
                    db,
                    organization_id
                )
            )


            if not agent_record:

                raise Exception(
                    "Agent not found. Create agent first."
                )


            print(
                "AZURE AGENT:",
                agent_record.azure_agent_name,
                agent_record.azure_agent_version
            )



            messages = [
                {
                    "role": "user",
                    "content": message
                }
            ]



            with DefaultAzureCredential() as credential:


                with AIProjectClient(
                    endpoint=self.project_endpoint,
                    credential=credential
                ) as project_client:


                    with project_client.get_openai_client() as openai_client:


                        response = (
                            openai_client
                            .responses
                            .create(

                                input=messages,

                                extra_body={

                                    "agent_reference": {

                                        "name":
                                        agent_record.azure_agent_name,

                                        "type":
                                        "agent_reference",

                                        "version":
                                        agent_record.azure_agent_version

                                    }

                                }

                            )
                        )



                        input_list = []



                        for item in response.output:


                            if item.type != "function_call":

                                continue



                            print(
                                "TOOL CALLED:",
                                item.name
                            )


                            arguments = json.loads(
                                item.arguments
                            )



                            if item.name == "knowledge_search":


                                result = (
                                    self.knowledge_service
                                    .search_knowledge(
                                        organization_id,
                                        arguments["query"]
                                    )
                                )



                            elif item.name == "get_available_slots":


                                result = get_available_slots(
                                    **arguments
                                )



                            elif item.name == "create_calendar_event":


                                result = create_calendar_event(
                                    **arguments
                                )


                            else:

                                continue



                            input_list.append(

                                FunctionCallOutput(

                                    type="function_call_output",

                                    call_id=item.call_id,

                                    output=json.dumps(result)

                                )

                            )



                        if input_list:


                            response = (
                                openai_client
                                .responses
                                .create(

                                    previous_response_id=response.id,

                                    input=input_list,

                                    extra_body={

                                        "agent_reference": {

                                            "name":
                                            agent_record.azure_agent_name,

                                            "type":
                                            "agent_reference",

                                            "version":
                                            agent_record.azure_agent_version

                                        }

                                    }

                                )
                            )



                        return {

                            "response":
                            response.output_text

                        }


        finally:

            db.close()