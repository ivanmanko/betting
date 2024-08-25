from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import enum
import decimal

class EventState(enum.Enum):
    NEW = 0
    FINISHED_WIN = 1
    FINISHED_LOSE = 2



class EventBase(BaseModel):
    coefficient: Optional[decimal.Decimal] = None
    deadline: Optional[datetime] = None  # Используем datetime для дедлайна

class EventCreate(EventBase):
    ...

class EventUpdate(EventBase):
    state: Optional[EventState] = None

class EventRead(EventUpdate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
