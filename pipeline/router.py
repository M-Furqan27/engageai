from fastapi import APIRouter

from pipeline.service import PipelineService
from pipeline.schemas import PipelineSetupRequest


router = APIRouter(
    prefix="/pipeline",
    tags=["Pipeline"]
)


pipeline_service = PipelineService()


@router.post("/setup")
async def setup_pipeline(
    request: PipelineSetupRequest
):
    
    

    result = await (
        pipeline_service
        .setup(
            request
        )
    )

    return {
        "status": "ready",
        "organization_id": request.organization_id
    }
