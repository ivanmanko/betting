import random
from datetime import datetime, timezone

import redis
import requests
from celery import shared_task
from config import settings
from dateutil import parser


class EventService:
    def __init__(self):
        self.redis_client = redis.from_url(settings.redis_url)

    @staticmethod
    def get_db_timezone():
        try:
            response = requests.get(f"http://{settings.line_provider_host}:{settings.line_provider_port}/timezone")
            response.raise_for_status()
            return response.json()["timezone"]
        except requests.RequestException as e:
            print(f"Failed to get database timezone: {e}")
            return None

    @staticmethod
    def get_current_time(db_timezone):
        try:
            current_time_response = requests.get(f"http://{settings.line_provider_host}:{settings.line_provider_port}/current-time")
            current_time_response.raise_for_status()
            current_time = parser.parse(current_time_response.json()["current_time"])

            # Конвертируем текущее время в временную зону базы данных и затем в UTC
            return current_time.astimezone(timezone.utc)
        except requests.RequestException as e:
            print(f"Failed to get current time: {e}")
            return None

    @staticmethod
    def get_events(created_after=30):
        try:
            events_response = requests.get(
                f"http://{settings.line_provider_host}:{settings.line_provider_port}/events",
                params={"created_after": created_after}
            )
            events_response.raise_for_status()
            return events_response.json()
        except requests.RequestException as e:
            print(f"Failed to get events: {e}")
            return []

    @staticmethod
    def update_event_state(event_id, new_state):
        try:
            update_event_response = requests.put(
                f"http://{settings.line_provider_host}:{settings.line_provider_port}/event/{event_id}",
                json={"state": new_state}
            )
            return update_event_response.status_code == 200
        except requests.RequestException as e:
            print(f"Failed to update Event ID: {event_id}")
            return False
        
    @shared_task
    def schedule_event_task(event_id: int):
        """Обновляет состояние события и обрабатывает ставки в момент дедлайна."""
        new_state = random.choice([1, 2])  # 1 - WON, 2 - LOST
        event_service.update_event_state(event_id, new_state)
        event_service.process_bets(event_id, new_state)

    @staticmethod
    def update_bet_state(bet_id, new_state):
        try:
            update_bet_response = requests.put(
                f"http://{settings.bet_maker_host}:{settings.bet_maker_port}/bet",
                json={"bet_id": bet_id, "state": new_state}
            )
            return update_bet_response.status_code == 200
        except requests.RequestException as e:
            print(f"Failed to update Bet ID: {bet_id}")
            return False

    def process_events(self, events, current_time):
        for event in events:
            event_deadline = parser.parse(event["deadline"])

            # Приводим оба времени к UTC перед сравнением
            event_deadline_utc = event_deadline.astimezone(timezone.utc)
            current_time_utc = current_time.astimezone(timezone.utc)

            print(f"Event ID: {event['id']} with Deadline: {event_deadline_utc} and Current Time: {current_time_utc}")
            print(event_deadline_utc <= current_time_utc)
            print(event["state"] == 0)
            print(not self.redis_client.sismember("processed_events", event["id"]))

            if event["state"] == 0 and not self.redis_client.sismember("processed_events", event["id"]):
                print(f"timer: {(event_deadline_utc - current_time_utc).total_seconds()}")
                self.schedule_event_task.apply_async(args=[event["id"]], countdown=(event_deadline_utc - current_time_utc).total_seconds())

    @staticmethod
    def process_bets(event_id, new_state):
        bets_response = requests.get(f"http://{settings.bet_maker_host}:{settings.bet_maker_port}/bets", params={"event_id": event_id})
        bets = bets_response.json()
        print(f'Found {len(bets)} bets for Event ID: {event_id}')
        for bet in bets:
            if EventService.update_bet_state(bet['id'], new_state):
                print(f"Updated Bet ID: {bet['id']} to state: {new_state}")
            else:
                print(f"Failed to update Bet ID: {bet['id']}")

event_service = EventService()