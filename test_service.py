from database.database import SessionLocal

from services.organization_service import OrganizationService



db = SessionLocal()


service = OrganizationService()


data = service.get_agent_context(
    db,
    1
)


print(data)