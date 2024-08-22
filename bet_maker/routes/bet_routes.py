from fastapi import APIRouter, HTTPException, Depends
from bet_maker.services.bet_service import BetService
from bet_maker.models.bet import Bet

router = APIRouter()

@router.get("/events")
async def get_events():
    # Реализация логики для получения событий из line-provider
    return []

@router.post("/bet")
async def create_new_bet(bet: Bet, bet_service: BetService = Depends()):
    if not bet.event_id:
        raise HTTPException(status_code=400, detail="Event ID is required")
    await bet_service.create_bet(bet)
    return {"bet_id": bet.bet_id}

@router.get("/bets")
async def get_bets(bet_service: BetService = Depends()):
    return await bet_service.get_all_bets()
