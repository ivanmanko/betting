# from dotenv import load_dotenv
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn
# from dotenv import load_dotenv

class LineProviderSettings(BaseSettings):
    host: str
    port: int

    class Config:
        env_prefix = 'LINE_PROVIDER_'

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
        env_prefix = 'POSTGRES_LINE_PROVIDER_'  # Префикс для настроек БД line_provider


class Settings(BaseSettings):
    db: DatabaseSettings = DatabaseSettings()
    database_echo: bool = False
    line_provider: LineProviderSettings = LineProviderSettings()

    class Config:
        env_file = ".env"
        extra = "ignore" 


# Инициализация настроек
settings = Settings()

print(settings)