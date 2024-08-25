from repositories.bet_repository import bet_repository, BetRepository
from models.bet import Bet
from schemas.bet import BetRead, BetUpdate
from schemas.bet import BetCreate
from typing import List, Optional
from datetime import datetime
from services.line_provider_service import LineProviderService

class BetService:
    def __init__(self, bet_repository: BetRepository, line_provider_service: LineProviderService):
        self.bet_repository = bet_repository
        self.line_provider_service = line_provider_service

    async def create_bet(self, bet: BetCreate):
        bet_id = await self.bet_repository.create_bet(bet)
        return BetRead(**bet.model_dump(), state=0, id=bet_id)

    async def get_all_bets(self, event_id: Optional[int] = None) -> List[Bet]:
        return await self.bet_repository.get_all_bets(event_id=event_id)

    async def get_active_events(self):
        return await self.line_provider_service.get_active_events()
    
    async def update_bet_state(self, bet_update: BetUpdate) -> Optional[BetRead]:
            bet = await self.bet_repository.update_bet_state(bet_update=bet_update)
            return BetRead.from_orm(bet) if bet else None
    
bet_service = BetService(bet_repository, LineProviderService())
