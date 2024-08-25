import uvicorn
from config import settings

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.bet_maker.host, port=settings.bet_maker.port)
