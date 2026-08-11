from agents.runtime import AgentRuntime


runtime = AgentRuntime()


def process_widget_message(
    organization_id,
    agent_id,
    visitor_id,
    message
):

    response = runtime.chat_from_widget(
        organization_id=organization_id,
        agent_id=agent_id,
        visitor_id=visitor_id,
        message=message
    )

    return response