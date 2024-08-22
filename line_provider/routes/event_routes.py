from fastapi import APIRouter, Path, HTTPException, Depends
from services.event_service import EventService
from models.event import Event
from db import get_db_session

router = APIRouter()


@router.get('/events')
async def list_events(event_service: EventService = Depends()):
    return await event_service.get_all_events()


@router.get('/event/{event_id}')
async def retrieve_event(event_id: str = Path(default=None), event_service: EventService = Depends()):
    event = await event_service.get_event_by_id(event_id)
    if event:
        return event
    raise HTTPException(status_code=404, detail="Event not found")


@router.put('/event')
async def create_event(event: Event, event_service: EventService = Depends()):
    await event_service.create_or_update_event(event)
    return {}
