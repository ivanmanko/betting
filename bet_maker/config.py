from pydantic_settings import BaseSettings
from pydantic import PostgresDsn
import os




class BetMakerSettings(BaseSettings):
    host: str
    port: int

    class Config:
        env_prefix = 'BET_MAKER_'  # Префикс для настроек bet_maker

class LineProviderSettings(BaseSettings):
    host: str
    port: int

    class Config:
        env_prefix = 'LINE_PROVIDER_'  # Префикс для настроек line_provider

class DatabaseSettings(BaseSettings):
    user: str
    password: str
    db: str
    host: str
    port: str

    @property
    def async_url(self) -> PostgresDsn:
        return (
            f"postgresql+asyncpg://{self.user}:{self.password}"
            f"@{self.host}:{self.port}/{self.db}"
        )

    @property
    def sync_url(self) -> PostgresDsn:
        return (
            f"postgresql+psycopg2://{self.user}:{self.password}"
            f"@{self.host}:{self.port}/{self.db}"
        )

    class Config:
        env_prefix = 'POSTGRES_BET_MAKER_'  # Префикс для настроек БД bet_maker

class Settings(BaseSettings):
    db: DatabaseSettings = DatabaseSettings()
    line_provider: LineProviderSettings = LineProviderSettings()
    bet_maker: BetMakerSettings = BetMakerSettings()
    database_echo: bool = False

    class Config:
        env_file = ".env"
        extra = "ignore"  # Добавляем игнорирование лишних переменных

# Инициализация настроек
settings = Settings()

print(settings)
