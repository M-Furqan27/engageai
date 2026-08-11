from tools.calendar_tools import get_available_slots


result = get_available_slots(
    business_id="1",
    visitor_id="visitor-101",
    name="Ali Khan",
    email="ali@example.com",
    message="I want to schedule a meeting"
)

print(result)