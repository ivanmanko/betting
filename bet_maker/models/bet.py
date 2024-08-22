from pydantic import BaseModel
from typing import List

class Bet(BaseModel):
    bet_id: str
    event_id: str
    amount: float
    status: str  # Can be "pending", "win", "lose"
