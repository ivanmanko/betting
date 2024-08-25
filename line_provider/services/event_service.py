from repositories.event_repository import EventRepository, event_repository
from schemas import EventCreate, EventRead
from models.event import Event
from typing import List, Optional
from datetime import datetime, timezone

class EventService:
    def __init__(self, repository: EventRepository):
        self.repository = repository

    async def create(self, event_data: EventCreate) -> EventRead:
        event = await self.repository.create(Event(**event_data.dict(), state=0))
        return EventRead.from_orm(event)
    
    async def update(self, event_id: str, event_data: EventCreate) -> EventRead:
        event_data_dict = event_data.dict(exclude_unset=True)
        if 'state' in event_data_dict:
            event_data_dict['state'] = event_data_dict['state'].value  # Преобразуем Enum в его значение
        
        updated_event = await self.repository.update(event_id, event_data_dict)
        return EventRead.from_orm(updated_event) if updated_event else None

    async def get_by_id(self, event_id: str) -> EventRead:
        event = await self.repository.get_by_id(event_id)
        return EventRead.from_orm(event) if event else None

    async def get_all(self, active: bool = False, created_after: Optional[int] = None):
        events = await self.repository.get_all(active=active, created_after=created_after)
        return [EventRead.from_orm(event) for event in events]
    
    async def get_active_events(self) -> List[EventRead]:
        db_time = await self.event_repository.get_current_db_time()
        events = await self.event_repository.get_active_events(db_time=db_time)
        return [EventRead.from_orm(event) for event in events]
    
    async def get_current_time(self) -> str:
        return await self.repository.get_current_time()
    
    async def get_timezone(self) -> str:
        return await self.repository.get_timezone()

event_service = EventService(event_repository)
