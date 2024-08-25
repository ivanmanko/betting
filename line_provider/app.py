import uvicorn
from config import settings

if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host=settings.line_provider.host, 
        port=settings.line_provider.port
                )
