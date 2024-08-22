from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from bet_maker.models.bet import Event
from sqlalchemy import insert, update

class EventRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_event(self, event: Event):
        stmt = insert(Event).values(
            event_id=event.event_id,
            coefficient=event.coefficient,
            deadline=event.deadline,
            state=event.state
        )
        await self.db_session.execute(stmt)
        await self.db_session.commit()

    async def update_event(self, event: Event):
        stmt = update(Event).where(Event.event_id == event.event_id).values(
            coefficient=event.coefficient,
            deadline=event.deadline,
            state=event.state
        )
        await self.db_session.execute(stmt)
        await self.db_session.commit()

    async def get_event_by_id(self, event_id: str) -> Event:
        stmt = select(Event).where(Event.event_id == event_id)
        result = await self.db_session.execute(stmt)
        return result.scalars().first()

    async def get_all_events(self):
        stmt = select(Event)
        result = await self.db_session.execute(stmt)
        return result.scalars().all()
