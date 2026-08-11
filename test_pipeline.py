import asyncio

from services.pipeline_service import PipelineService


async def main():

    pipeline = PipelineService()


    result = await pipeline.setup(

        organization_id=1,

        text="""
        ABC Travel provides travel consultation,
        booking support and customer assistance.

        Refund Policy:
        Customers can request refunds within 7 days.
        """,

        urls=[],

        pdfs=[]

    )


    print("\nPipeline Completed")

    print(result)



if __name__ == "__main__":

    asyncio.run(main())