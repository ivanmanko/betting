from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from bet_maker.models.bet import Bet
from sqlalchemy import insert, update

class BetRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_bet(self, bet: Bet):
        stmt = insert(Bet).values(
            bet_id=bet.bet_id,
            event_id=bet.event_id,
            amount=bet.amount,
            status=bet.status
        )
        await self.db_session.execute(stmt)
        await self.db_session.commit()

    async def get_all_bets(self):
        stmt = select(Bet)
        result = await self.db_session.execute(stmt)
        return result.scalars().all()
