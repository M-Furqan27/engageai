from tools.calendar_tools import create_calendar_event


result = create_calendar_event(
    visitor_id="visitor-101",
    name="Ali Khan",
    email="ali@example.com",
    slot_start="2026-08-07T10:00:00.000Z",
    slot_end="2026-08-07T10:30:00.000Z"
)


print(result)