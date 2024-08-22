from sqlalchemy import Column, String, Float, Integer, Enum
from sqlalchemy.ext.declarative import declarative_base
import enum
from pydantic import BaseModel
import decimal

# Определение базового класса для моделей SQLAlchemy
Base = declarative_base()

class EventState(enum.Enum):
    NEW = "new"
    FINISHED_WIN = "finished_win"
    FINISHED_LOSE = "finished_lose"

# SQLAlchemy модель для таблицы Event
class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(String, unique=True, index=True)
    coefficient = Column(Float)
    deadline = Column(Integer)
    state = Column(Enum(EventState))

# Pydantic модель для валидации данных
class EventCreate(BaseModel):
    event_id: str
    coefficient: decimal.Decimal
    deadline: int
    state: EventState

    class Config:
        orm_mode = True
