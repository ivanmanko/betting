from fastapi import APIRouter, Path, HTTPException
from line_provider.services.event_service import get_event_by_id, get_events, create_or_update_event
from line_provider.models.event import Event

router = APIRouter()

@router.get('/events')
async def list_events():
    return get_events()

@router.get('/event/{event_id}')
async def retrieve_event(event_id: str = Path(default=None)):
    event = get_event_by_id(event_id)
    if event:
        return event
    raise HTTPException(status_code=404, detail="Event not found")

@router.put('/event')
async def create_event(event: Event):
    create_or_update_event(event)
    return {}
