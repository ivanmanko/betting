from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from config import settings

class DatabaseHelper:
    def __init__(self, url: str, echo: bool = False):
        # Создайте асинхронный движок
        self.engine = create_async_engine(
            url=url,
            echo=echo,
        )
        # Создайте sessionmaker, указывая class_=AsyncSession
        self.session_factory = sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
            class_=AsyncSession
        )

    def get_scoped_session(self):
        # Используйте скоуп для привязки сессии к текущей задаче
        session = sessionmaker(
            bind=self.engine,
            class_=AsyncSession
        )(
            expire_on_commit=False
        )
        return session

    async def session_dependency(self) -> AsyncSession:
        # Предоставление сессии для зависимости в FastAPI
        async with self.session_factory() as session:
            yield session
            # Закрытие сессии
            await session.close()

    async def scoped_session_dependency(self) -> AsyncSession:
        # Использование сессии в скоупе
        session = self.get_scoped_session()
        yield session
        await session.close()

# Создайте экземпляр DatabaseHelper с вашими настройками
db_helper = DatabaseHelper(
    url=settings.db.async_url,
    echo=settings.database_echo,
)
