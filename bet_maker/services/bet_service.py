from bet_maker.repositories.bet_repository import BetRepository
from bet_maker.models.bet import Bet
from typing import List


class BetService:
    def __init__(self, bet_repository: BetRepository):
        self.bet_repository = bet_repository

    async def create_bet(self, bet: Bet):
        await self.bet_repository.create_bet(bet)

    async def get_all_bets(self) -> List[Bet]:
        return await self.bet_repository.get_all_bets()
