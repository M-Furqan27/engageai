from agents.runtime import AgentRuntime


def main():

    runtime = AgentRuntime()

    runtime.chat(
        organization_id=3,
        agent_id=24,
        visitor_id="visitor_001",
        message="I want to schedule a vehicle inspection on 2026-08-10"
    )


if __name__ == "__main__":
    main()