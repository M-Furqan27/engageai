

from typing import List

from uuid import UUID

from fastapi import APIRouter, File, Form, UploadFile

from knowledge_base.service import KnowledgeBaseService

router = APIRouter(
    prefix="/knowledge-base",
    tags=["Knowledge Base"],
)

service = KnowledgeBaseService()


@router.post("/create")
async def create_knowledge_base(
    organization_id: UUID = Form(...),
    text: str = Form(""),
    url: str = Form(""),
    pdfs: List[UploadFile] = File(...),
):

    urls = [u.strip() for u in url.split(",") if u.strip()]

    kb = await service.create(
        organization_id=organization_id,
        text=text,
        urls=urls,
        pdfs=pdfs,
    )

    # return {
    #     "organization_id": kb.organization_id,
    #     "sources": [
    #         {
    #             "source_type": s.source_type,
    #             "source_name": s.source_name,
    #             "chunk_count": len(s.chunks),
    #         }
    #         for s in kb.sources
    #     ],
    # }
    
    return {
    "organization_id": kb.organization_id,
    "sources": [
        {
            "source_type": s.source_type,
            "source_name": s.source_name,
            "chunk_count": len(s.chunks),
            "sections": sorted({
                c.section for c in s.chunks if c.section
            }),
        }
        for s in kb.sources
    ],
}