from database.models import Agent



class AgentService:


    def save_agent(
        self,
        db,
        organization_id,
        agent,
        prompt
    ):


        record = Agent(

            organization_id=organization_id,

            azure_agent_name=agent.name,

            azure_agent_version=str(
                agent.version
            ),

            system_prompt=prompt

        )


        db.add(record)

        db.commit()

        db.refresh(record)


        return record



    def get_agent(
        self,
        db,
        organization_id
    ):


        return (

            db.query(Agent)

            .filter(
                Agent.organization_id == organization_id
            )

            .first()

        )