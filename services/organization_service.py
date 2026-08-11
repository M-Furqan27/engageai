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

            representatives.append({

                "name": rep.representative_name,

                "email": rep.company_email,

                "service": {
                    "name": rep.service,
                    "description": rep.service_description
                }

            })



        return {


            "organization": {

                "name":
                organization.organization_name,

                "description":
                organization.description

            },


            "representatives":
            representatives

        }