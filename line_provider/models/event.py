from sqlalchemy import Column, Float, Integer, Enum, TIMESTAMP
from models.base import Base
from sqlalchemy.types import TypeDecorator

class EventStateEnum(TypeDecorator):
    impl = Enum('0', '1', '2', name='eventstate')

    def process_bind_param(self, value, dialect):
        if value is not None:
            return str(value)
        return None

    def process_result_value(self, value, dialect):
        if value is not None:
            return int(value)
        return None

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    coefficient = Column(Float)
    deadline = Column(TIMESTAMP(timezone=True))  # Используем TIMESTAMP WITH TIME ZONE для дедлайна
    state = Column(EventStateEnum)