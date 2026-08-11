import os
import requests
import re

from dotenv import load_dotenv


load_dotenv()


AVAILABLE_SLOTS_WEBHOOK = os.getenv(
    "N8N_AVAILABLE_SLOTS_WEBHOOK"
)


CREATE_EVENT_WEBHOOK = os.getenv(
    "N8N_CREATE_EVENT_WEBHOOK"
)



def get_available_slots(
    organization_id: str,
    representative_id: str,
    proposed_date: str,
    duration_minutes: int = 30,
    offset: int = 0,
    limit: int = 3,
):
    payload = {
        "organization_id": organization_id,
        "representative_id": representative_id,
        "proposed_date": proposed_date,
        "duration_minutes": duration_minutes,
        "offset": offset,
        "limit": limit,
    }

    response = requests.post(
        AVAILABLE_SLOTS_WEBHOOK,
        json=payload,
        timeout=30,
    )

    response.raise_for_status()

    print("STATUS:", response.status_code)
    print("RAW RESPONSE:", response.text)

    return response.json()


def create_calendar_event(
    representative_id: str,
    customer_name: str,
    customer_email: str,
    service: str,
    slot_start: str,
    slot_end: str
):

    customer_email = re.sub(
        r"\[([^\]]+)\]\(mailto:[^)]+\)",
        r"\1",
        customer_email
    )

    payload = {
        "representative_id": representative_id,
        "customer_name": customer_name,
        "customer_email": customer_email,
        "service": service,
        "slot_start": slot_start,
        "slot_end": slot_end
    }


    response = requests.post(
        CREATE_EVENT_WEBHOOK,
        json=payload,
        timeout=30,
    )


    response.raise_for_status()


    return response.json()