from pydantic import BaseModel, Field
from enum import Enum


class BetStateEnum(int, Enum):
    NOT_PLAYED = 0  # Ещё не сыграла
    WON = 1         # Выиграла
    LOST = 2        # Проиграла


class BetBase(BaseModel):
    event_id: int
    amount: float = Field(..., gt=0, description="Amount must be a positive number with two decimal places")


class BetCreate(BetBase):
    pass

class BetUpdate(BaseModel):
    bet_id: int
    state: BetStateEnum


class BetRead(BetBase):
    id: int
    state: BetStateEnum

    class Config:
        from_attributes = True
