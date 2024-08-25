from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert, update
from models.bet import Bet
from db import db_helper, DatabaseHelper
from typing import Optional

class BetRepository:
    def __init__(self, db_helper: DatabaseHelper):
        self.db_helper = db_helper

    async def create_bet(self, bet: Bet):
        async for session in self.db_helper.session_dependency():
            stmt = insert(Bet).values(
                event_id=bet.event_id,
                amount=bet.amount,
                state=0
            )
            result = await session.execute(stmt)
            await session.commit()
            return result.inserted_primary_key[0]  # Возвращаем уникальный идентификатор

    async def get_all_bets(self, event_id: Optional[int] = None):
        async for session in self.db_helper.session_dependency():
            stmt = select(Bet)
            if event_id is not None:
                stmt = stmt.filter(Bet.event_id == event_id)
            result = await session.execute(stmt)
            return result.scalars().all()
        
    async def update_bet_state(self, bet_update) -> Optional[Bet]:
        async for session in self.db_helper.session_dependency():
            bet = await session.get(Bet, bet_update.bet_id)
            if not bet:
                return None
            bet.state = bet_update.state.value
            session.add(bet)
            await session.commit()
            await session.refresh(bet)
            
            return bet
        
bet_repository = BetRepository(db_helper)   
    
