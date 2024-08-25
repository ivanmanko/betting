from celery import shared_task
from event_service import event_service
import pytz



@shared_task
def run_check_events_deadline():
    db_timezone_str = event_service.get_db_timezone()
    if not db_timezone_str:
        return
    db_timezone = pytz.timezone(db_timezone_str)

    current_time = event_service.get_current_time(db_timezone)
    if not current_time:
        return
    print(f"Current time from DB: {current_time}")

    events = event_service.get_events(created_after=30)
    print(f"Fetched {len(events)} events")

    event_service.process_events(events, current_time)