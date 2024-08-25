from fastapi import FastAPI
from routes.event_routes import router as event_router

app = FastAPI()

app.include_router(event_router)

@app.on_event("startup")
async def startup_event():
    ...

