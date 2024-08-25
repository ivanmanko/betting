from fastapi import FastAPI
from routes.bet_routes import router as bet_router

app = FastAPI()

# Подключаем маршруты
app.include_router(bet_router)


@app.on_event("startup")
async def startup_event():
    ...

