from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import enum
import decimal

class EventState(enum.Enum):
    NEW = 1
    FINISHED_WIN = 2
    FINISHED_LOSE = 3

class EventBase(BaseModel):
    coefficient: Optional[decimal.Decimal] = None
    deadline: Optional[datetime] = None  # Используем datetime для дедлайна
    state: Optional[EventState] = None

class EventCreate(EventBase):
    pass

class EventRead(EventBase):
    id: int

    class Config:
        orm_mode = True

# Если вам все еще нужен класс Event, вы можете определить его так:
class Event(EventBase):
    id: int