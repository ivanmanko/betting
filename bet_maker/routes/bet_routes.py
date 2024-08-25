from fastapi import APIRouter, HTTPException, Depends, Body
from services.bet_service import BetService, bet_service 
from schemas.event import EventRead
from schemas.bet import BetCreate, BetRead, BetUpdate
from typing import List, Optional

router = APIRouter()

@router.get('/events', response_model=List[EventRead])
async def list_events(
    service: BetService = Depends(lambda: bet_service)
):
    return await service.get_active_events()

@router.post("/bet", response_model=BetRead)
async def create_new_bet(bet: BetCreate, bet_service: BetService = Depends(lambda: bet_service)):
    if not bet.event_id:
        raise HTTPException(status_code=400, detail="Event ID is required")
    
    created_bet = await bet_service.create_bet(bet)
    return created_bet

@router.get("/bets")
async def get_bets(
    event_id: Optional[int] = None,
    bet_service: BetService = Depends(lambda: bet_service)
):
    return await bet_service.get_all_bets(event_id=event_id)


@router.put("/bet", response_model=BetRead)
async def update_bet_state(
    bet_update: BetUpdate = Body(...),
    bet_service: BetService = Depends(lambda: bet_service)
):
    print(f"Received request to update bet with id: {bet_update.bet_id} to state: {bet_update.state}")
    # try:
    updated_bet = await bet_service.update_bet_state(bet_update=bet_update)
    if not updated_bet:
        raise HTTPException(status_code=404, detail="Bet not found")
    return updated_bet
 