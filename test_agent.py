from agents.main_agent import MainAgent

from agents.runtime import AgentRuntime




def main():


    # Create agent

    agent_creator = MainAgent()


    agent = (

        agent_creator
        .create_agent(

            organization_id=3

        )

    )



    print("Agent Created:")


    # print(agent.azure_agent_name)

    # print(agent.azure_agent_version)


    # print(agent.name)
    # print(agent.version)

    # Start chat

    runtime = AgentRuntime()


    runtime.chat(
            organization_id=3,
            agent_id=24,
            visitor_id="visitor_001",
            message="I want to schedule a vehicle inspection on 2026-08-10"
        )




if __name__ == "__main__":

    main()