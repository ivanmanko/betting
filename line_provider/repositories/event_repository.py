from db import db_helper
from models.event import Event
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy import func

class EventRepository:
    def __init__(self):
        self.db_helper = db_helper

    async def get_current_time_in_db(self):
        """
        Получение текущего времени из базы данных через db_helper.
        """
        async for session in self.db_helper.session_dependency():
            current_time_in_db = await session.execute(select(func.now()))
            return current_time_in_db.scalar()

    async def create(self, event: Event):
        async for session in self.db_helper.session_dependency():
            session.add(event)
            await session.commit()
            await session.refresh(event)
            return event

    async def get_by_id(self, event_id: str):
        async for session in self.db_helper.session_dependency():
            return await session.get(Event, event_id)

    async def get_all(self, active: bool = False, created_after: Optional[int] = None):
        async for session in self.db_helper.session_dependency():
            stmt = select(Event)
            if active:
                stmt = stmt.filter(Event.state == 0)
            if created_after is not None:
                # Получаем текущее время из базы данных
                current_time_stmt = select(func.now())
                current_time_result = await session.execute(current_time_stmt)
                current_time = current_time_result.scalar()

                # Вычисляем время отсечения
                cutoff_time = current_time - timedelta(seconds=created_after)
                stmt = stmt.filter(Event.created_at > cutoff_time)

            result = await session.execute(stmt)
            return result.scalars().all()
        
    async def update(self, event_id: str, event_data: dict):
                # If the deadline is naive, make it aware
        async for session in self.db_helper.session_dependency():
            query = (
                update(Event)
                .where(Event.id == event_id)
                .values(**event_data)
                .execution_options(synchronize_session="fetch")
            )
            await session.execute(query)
            await session.commit()
            
            # Вернуть обновленный объект
            updated_event = await session.get(Event, event_id)
            return updated_event
        
    async def get_current_time(self) -> datetime:
        async for session in db_helper.session_dependency():
            stmt = select(func.now())
            result = await session.execute(stmt)
            return result.scalar()
        
    async def get_timezone(self) -> str:
        async for session in self.db_helper.session_dependency():
            stmt = select(func.current_setting('TIMEZONE'))
            result = await session.execute(stmt)
            timezone = result.scalar()
            return timezone
        
event_repository = EventRepository()
