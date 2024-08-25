import requests
import pytz
from config import settings
from dateutil import parser

def get_db_timezone():
    try:
        response = requests.get(f"http://{settings.line_provider_host}:{settings.line_provider_port}/timezone")
        response.raise_for_status()
        return pytz.timezone(response.json()["timezone"])
    except requests.RequestException as e:
        print(f"Failed to get database timezone: {e}")
        return pytz.UTC  # Фолбэк на UTC

def get_current_time(db_timezone):
    try:
        current_time_response = requests.get(f"http://{settings.line_provider_host}:{settings.line_provider_port}/current-time")
        current_time_response.raise_for_status()
        current_time = parser.parse(current_time_response.json()["current_time"])
        return current_time.astimezone(db_timezone)
    except requests.RequestException as e:
        print(f"Failed to get current time: {e}")
        return None
