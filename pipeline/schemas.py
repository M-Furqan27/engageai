from pydantic import BaseModel
from uuid import UUID


class RepresentativeInput(BaseModel):

    name: str

    email: str

    service: str



class PipelineSetupRequest(BaseModel):

    organization_id: UUID

    organization_name: str

    business_type: str

    description: str


    representative: RepresentativeInput


    text: str | None = None

    documents: list[str] = []