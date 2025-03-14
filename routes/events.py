from typing import List
from fastapi import APIRouter
from services.event_service import EventService
from db.schemas.event_schema import EventCreate, EventResponse

router = APIRouter(prefix="/events", tags=["Events"])

@router.post("/create", response_model=EventResponse)
def create_event(event: EventCreate):
    """Create a new event and add it to the database."""
    return EventService.create_event(event)

@router.get("/all", response_model=List[EventResponse])
def get_all_events():
    """Fetch all events stored in the database."""
    return EventService.get_all_events()

@router.get("/{id}", response_model=EventResponse)
def get_event(id: int):
    """Fetch a specific event by ID."""
    return EventService.get_event(id)

@router.put("/{id}", response_model=EventResponse)
def update_event(id: int, updated_event: EventCreate):
    """Update an existing event."""
    return EventService.update_event(id, updated_event)

@router.delete("/{id}")
def delete_event(id: int):
    """Delete an event by ID."""
    return EventService.delete_event(id)

@router.post("/trigger/{id}")
def trigger_event(id: int):
    """Triggers an event and logs the response."""
    return EventService.trigger_event(id)
