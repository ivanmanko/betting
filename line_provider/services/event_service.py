from line_provider.repositories.event_repository import EventRepository
from line_provider.models.event import Event
from typing import List

class EventService:
    def __init__(self, event_repository: EventRepository):
        self.event_repository = event_repository

    async def create_or_update_event(self, event: Event):
        existing_event = await self.event_repository.get_event_by_id(event.event_id)
        if existing_event:
            await self.event_repository.update_event(event)
        else:
            await self.event_repository.create_event(event)

    async def get_event_by_id(self, event_id: str) -> Event:
        return await self.event_repository.get_event_by_id(event_id)

    async def get_all_events(self) -> List[Event]:
        return await self.event_repository.get_all_events()
