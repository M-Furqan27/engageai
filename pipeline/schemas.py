from pydantic import BaseModel


class RepresentativeInput(BaseModel):

    name: str

    email: str

    service: str



class PipelineSetupRequest(BaseModel):

    organization_id: int

    organization_name: str

    business_type: str

    description: str


    representative: RepresentativeInput


    text: str | None = None

    documents: list[str] = []