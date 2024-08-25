from sqlalchemy import Column, Integer, String, Float, Enum
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

class Bet(Base):
    __tablename__ = 'bets'
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, nullable=False)  # Идентификатор события
    amount = Column(Float, nullable=False)  # Сумма ставки
    state = Column(EventStateEnum, nullable=False)  # Состояние ставки
    # Другие поля...