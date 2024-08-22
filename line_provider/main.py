from fastapi import FastAPI
from routes.event_routes import router as event_router
import models.event as event_models
from db import engine

app = FastAPI()

app.include_router(event_router)

@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        # Здесь создается таблица, если ее нет
        await conn.run_sync(event_models.Base.metadata.create_all)
