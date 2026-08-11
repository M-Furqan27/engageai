import asyncio

from knowledge_base.service import KnowledgeBaseService

from fastapi import UploadFile

from pathlib import Path



async def main():


    kb = KnowledgeBaseService()


    pdf_path = Path(
        "ABC_Travel_Knowledge_Base.pdf"
    )


    pdf_file = UploadFile(
        filename=pdf_path.name,

        file=open(
            pdf_path,
            "rb"
        )
    )


    result = await kb.create(

        organization_id=1,

        text=None,

        urls=[],

        pdfs=[
            pdf_file
        ]

    )


    print(
        "Knowledge Base Created"
    )

    print(result)



if __name__ == "__main__":

    asyncio.run(main())