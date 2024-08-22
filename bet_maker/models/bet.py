import decimal
import enum
from pydantic import BaseModel
from typing import Optional


class EventState(enum.Enum):
    NEW = "new"
    FINISHED_WIN = "finished_win"
    FINISHED_LOSE = "finished_lose"


class Event(BaseModel):
    event_id: str
    coefficient: decimal.Decimal
    deadline: int
    state: EventState
