from sqlalchemy.orm import Session


from database.models import (
    Organization
)



class OrganizationService:


    def get_agent_context(
        self,
        db: Session,
        organization_id: int
    ):


        organization = (

            db.query(Organization)

            .filter(
                Organization.organization_id == organization_id
            )

            .first()

        )


        if not organization:

            raise Exception(
                "Organization not found"
            )



        representatives = []



        for rep in organization.representatives:


            services = []


            for service in rep.services:

                services.append({

                    "name":
                    service.name,


                    "description":
                    service.description

                })



            representatives.append({

                "name":
                rep.name,


                "email":
                rep.email,


                "services":
                services

            })




        return {


            "organization": {


                "name":
                organization.name,


                "description":
                organization.description

            },


            "representatives":
            representatives

        }