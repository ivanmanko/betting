import aiohttp
from config import settings

class LineProviderService:
    async def get_active_events(self):
        url = f"http://{settings.line_provider.host}:{settings.line_provider.port}/api/events"
        params = {'active': 'true'}  # Добавляем параметр active=true
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return []
