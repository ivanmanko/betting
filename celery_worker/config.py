from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    line_provider_host: str
    line_provider_port: int
    bet_maker_host: str
    bet_maker_port: int
    redis_host: str  
    redis_port: int 
    redis_db: int = 1 

    @property
    def redis_url(self):
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"

    class Config:
        env_prefix = 'CELERY_WORKER_'  # Префикс для всех переменных
        env_file = ".env"

settings = Settings()
