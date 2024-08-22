from fastapi import FastAPI
from routes.bet_routes import router as bet_router
import models.bet as bet_models
from db import engine

app = FastAPI()

# Подключаем маршруты
app.include_router(bet_router)


@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        # Здесь создается таблица, если ее нет
        await conn.run_sync(bet_models.Base.metadata.create_all)
