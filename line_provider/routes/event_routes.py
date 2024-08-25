from fastapi import APIRouter, Path, HTTPException, Depends
from services.event_service import event_service
from schemas import EventCreate, EventRead, EventUpdate
from typing import List
from services.event_service import EventService
from typing import Optional
from fastapi.param_functions import Query

router = APIRouter()


@router.get('/events', response_model=List[EventRead])
async def list_events(
    service: EventService = Depends(lambda: event_service), 
    active: Optional[bool] = Query(default=False, description="If true, only active events are returned"),
    created_after: Optional[int] = Query(None, description="If provided, only events created after this timestamp are returned"),
):
    return await service.get_all(active=active, created_after=created_after)

@router.get("/timezone")
async def get_timezone(service: EventService = Depends(lambda: event_service)):
    timezone = await service.get_timezone()
    return {"timezone": timezone}


@router.get('/event/{event_id}', response_model=EventRead)
async def retrieve_event(event_id: int = Path(...), service: EventService = Depends(lambda: event_service)):
    event = await service.get_by_id(event_id)
    if event:
        return event
    raise HTTPException(status_code=404, detail="Event not found")

@router.post('/event', response_model=EventRead)
async def create_event(event: EventCreate, service: EventService = Depends(lambda: event_service)):
    return await service.create(event)

@router.put('/event/{event_id}', response_model=EventRead)
async def update_event(event_id: int, event: EventUpdate, service: EventService = Depends(lambda: event_service)):
    try:
        return await service.update(event_id, event)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    

@router.get('/current-time')
async def get_current_time(service: EventService = Depends(lambda: event_service)):
    return {"current_time": await service.get_current_time()}
