import os
import json

from dotenv import load_dotenv

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

from openai.types.responses.response_input_param import FunctionCallOutput

from database.database import get_session

from services.agent_service import AgentService
from services.knowledge_service import KnowledgeService

from conversations.service import (
    start_or_get_conversation,
    add_user_message,
    add_assistant_message,
    get_conversation_history
)

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



    def chat(
        self,
        organization_id,
        agent_id,
        visitor_id,
        lead_id=None,
    ):


        db = get_session()


        conversation_record = start_or_get_conversation(
            db=db,
            organization_id=organization_id,
            agent_id=agent_id,
            lead_id=lead_id,
            visitor_id=visitor_id,
        )

        conversation_record.azure_conversation_id = None
        db.commit()

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



            with DefaultAzureCredential() as credential:


                with AIProjectClient(

                    endpoint=self.project_endpoint,

                    credential=credential

                ) as project_client:



                    with project_client.get_openai_client() as openai_client:



                        # -------------------------------
                        # Azure Conversation Memory
                        # -------------------------------

                        # if conversation_record.azure_conversation_id:


                        #     azure_conversation_id = (
                        #         conversation_record
                        #         .azure_conversation_id
                        #     )


                        # else:


                        #     conversation = (

                        #         openai_client
                        #         .conversations
                        #         .create()

                        #     )


                        #     azure_conversation_id = (
                        #         conversation.id
                        #     )


                        #     conversation_record.azure_conversation_id = (
                        #         azure_conversation_id
                        #     )


                        #     db.commit()



                        print(
                            "\nAgent Ready\n"
                        )



                        user_input = message



                        add_user_message(
                            db=db,
                            conversation_id=conversation_record.id,
                            message_text=user_input,
                            metadata=None,
                        )
                        
                        history = get_conversation_history(
                            db=db,
                            conversation_id=conversation_record.id
                        )

                        messages = []

                        for message in history:

                            messages.append(
                                {
                                    "role": message.sender_type,
                                    "content": message.message_text
                                }
                            )


                        messages.append(
                            {
                                "role": "user",
                                "content": user_input
                            }
                        )


                        input_list = []



                        response = (

                            openai_client
                            .responses
                            .create(

                                extra_body={

                                    "agent_reference":{

                                        "name":
                                        agent_record.azure_agent_name,

                                        "type":
                                        "agent_reference"

                                    }

                                },


                                input=messages

                            )
                        )

                        for item in response.output:

                            if item.type != "function_call":
                                continue



                            if item.type == "function_call":


                                print(
                                    "TOOL CALLED:",
                                    item.name
                                )



                                # -------------------------
                                # Knowledge Tool
                                # -------------------------

                                if item.name == "knowledge_search":


                                    arguments = json.loads(
                                        item.arguments
                                    )


                                    result = (

                                        self.knowledge_service
                                        .search_knowledge(

                                            organization_id,

                                            arguments["query"]

                                        )

                                    )


                                    input_list.append(

                                        FunctionCallOutput(

                                            type=
                                            "function_call_output",

                                            call_id=
                                            item.call_id,

                                            output=
                                            json.dumps(result)

                                        )

                                    )



                                # -------------------------
                                # Available Slots Tool
                                # -------------------------

                                elif item.name == "get_available_slots":
                                    result = get_available_slots(
                                            organization_id=arguments["organization_id"],
                                            representative_id=arguments["representative_id"],
                                            proposed_date=arguments["proposed_date"],
                                            duration_minutes=arguments["duration_minutes"],
                                            offset=arguments["offset"],
                                            limit=arguments["limit"]
                                        )


                                    input_list.append(

                                        FunctionCallOutput(

                                            type=
                                            "function_call_output",

                                            call_id=
                                            item.call_id,

                                            output=
                                            json.dumps(result)

                                        )

                                    )



                                # -------------------------
                                # Create Event Tool
                                # -------------------------

                                elif item.name == "create_calendar_event":


                                    arguments = json.loads(
                                        item.arguments
                                    )


                                    result = create_calendar_event(

                                        arguments["visitor_id"],

                                        arguments["name"],

                                        arguments["email"],

                                        arguments["slot_start"],

                                        arguments["slot_end"]

                                    )



                                    input_list.append(

                                        FunctionCallOutput(

                                            type=
                                            "function_call_output",

                                            call_id=
                                            item.call_id,

                                            output=
                                            json.dumps(result)

                                        )

                                    )



                            # -------------------------
                            # Send Tool Results Back
                            # -------------------------

                            if input_list:
                                
                                print("INPUT LIST:")
                                print(input_list)
                                
                                response = (

                                    openai_client
                                    .responses
                                    .create(

                                        previous_response_id=response.id,

                                        input=input_list,

                                        extra_body={
                                            "agent_reference":{
                                                "name": agent_record.azure_agent_name,
                                                "type":"agent_reference"
                                            }
                                        }
                                    )
                                )



                            if response.output_text:


                                print(
                                    "\nAGENT:",
                                    response.output_text
                                )


                                add_assistant_message(

                                    db=db,

                                    conversation_id=
                                    conversation_record.id,

                                    message_text=
                                    response.output_text,

                                    metadata=None,

                                )


                            else:

                                print(
                                    "NO FINAL TEXT RESPONSE"
                                )

                                print(
                                    response.output
                                )



        finally:

            db.close()
    
    # def chat(
    #     self,
    #     organization_id,
    #     agent_id,
    #     visitor_id,
    #     message,
    #     lead_id=None,
    # ):

    #     db = get_session()

    #     conversation_record = start_or_get_conversation(
    #         db=db,
    #         organization_id=organization_id,
    #         agent_id=agent_id,
    #         lead_id=lead_id,
    #         visitor_id=visitor_id,
    #     )

    #     try:

    #         agent_record = (
    #             self.agent_service
    #             .get_agent(
    #                 db,
    #                 organization_id
    #             )
    #         )

    #         if not agent_record:
    #             raise Exception(
    #                 "Agent not found. Create agent first."
    #             )


    #         with DefaultAzureCredential() as credential:

    #             with AIProjectClient(
    #                 endpoint=self.project_endpoint,
    #                 credential=credential
    #             ) as project_client:


    #                 with project_client.get_openai_client() as openai_client:


    #                     print("\nAgent Ready\n")


    #                     user_input = message


    #                     add_user_message(
    #                         db=db,
    #                         conversation_id=conversation_record.id,
    #                         message_text=user_input,
    #                         metadata=None,
    #                     )


    #                     response = (
    #                         openai_client
    #                         .responses
    #                         .create(

    #                             extra_body={
    #                                 "agent_reference": {
    #                                     "name": agent_record.azure_agent_name,
    #                                     "type": "agent_reference"
    #                                 }
    #                             },

    #                             input=[
    #                                 {
    #                                     "role": "user",
    #                                     "content": user_input
    #                                 }
    #                             ]
    #                         )
    #                     )


    #                     input_list = []


    #                     for item in response.output:


    #                         if item.type == "function_call":


    #                             print(
    #                                 "TOOL CALLED:",
    #                                 item.name
    #                             )


    #                             arguments = json.loads(
    #                                 item.arguments
    #                             )


    #                             if item.name == "knowledge_search":

    #                                 result = (
    #                                     self.knowledge_service
    #                                     .search_knowledge(
    #                                         organization_id,
    #                                         arguments["query"]
    #                                     )
    #                                 )


    #                             elif item.name == "get_available_slots":
    #                                 result = get_available_slots(
    #                                         organization_id=arguments["organization_id"],
    #                                         representative_id=arguments["representative_id"],
    #                                         proposed_date=arguments["proposed_date"],
    #                                         duration_minutes=arguments["duration_minutes"],
    #                                         offset=arguments["offset"],
    #                                         limit=arguments["limit"]
    #                                     )
    

    #                             elif item.name == "create_calendar_event":

    #                                 result = create_calendar_event(
    #                                     arguments["visitor_id"],
    #                                     arguments["name"],
    #                                     arguments["email"],
    #                                     arguments["slot_start"],
    #                                     arguments["slot_end"]
    #                                 )


    #                             else:
    #                                 continue



    #                             input_list.append(

    #                                 FunctionCallOutput(

    #                                     type="function_call_output",

    #                                     call_id=item.call_id,

    #                                     output=json.dumps(result)

    #                                 )

    #                             )



    #                     if input_list:


    #                         response = (
    #                             openai_client
    #                             .responses
    #                             .create(

    #                                 previous_response_id=response.id,

    #                                 input=input_list,

    #                                 extra_body={
    #                                     "agent_reference": {
    #                                         "name": agent_record.azure_agent_name,
    #                                         "type": "agent_reference"
    #                                     }
    #                                 }
    #                             )
    #                         )



    #                     if response.output_text:


    #                         add_assistant_message(
    #                             db=db,
    #                             conversation_id=conversation_record.id,
    #                             message_text=response.output_text,
    #                             metadata=None,
    #                         )


    #                         return response.output_text



    #                     return None


    #     finally:

    #         db.close()