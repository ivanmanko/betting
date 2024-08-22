from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, String, Float, Enum, Integer
import enum

DATABASE_URL = "postgresql+asyncpg://user:password@postgres/bet_maker_db"

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

# Определение модели для базы данных
Base = declarative_base()


class BetStatus(enum.Enum):
    PENDING = "pending"
    WIN = "win"
    LOSE = "lose"


class Bet(Base):
    __tablename__ = "bets"

    id = Column(Integer, primary_key=True, index=True)
    bet_id = Column(String, unique=True, index=True)
    event_id = Column(String, index=True)
    amount = Column(Float)
    status = Column(Enum(BetStatus))


# Функция для получения сессии базы данных
async def get_db_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session
