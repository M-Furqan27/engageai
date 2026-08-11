from database.models import Agent



class AgentService:


    def save_agent(
        self,
        db,
        organization_id,
        agent,
        prompt
    ):

        agent_link = (
            f"https://your-portal-domain.com/widget/{organization_id}"
        )


        record = Agent(

            organization_id=organization_id,

            azure_agent_name=agent.name,

            azure_agent_version=str(
                agent.version
            ),

            system_prompt=prompt,

            agent_link=agent_link

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