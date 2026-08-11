import asyncio

from knowledge_base.service import KnowledgeBaseService


async def main():

    kb = KnowledgeBaseService()


    result = await kb.create(

        organization_id=1,

        text="""
        ABC Travel provides travel consultation,
        booking support and customer assistance.

        Refund policy:
        Customers can request refunds within 7 days.
        """,

        urls=[],

        pdfs=[]

    )


    print("Knowledge uploaded successfully")
    print(result)



if __name__ == "__main__":

    asyncio.run(main())