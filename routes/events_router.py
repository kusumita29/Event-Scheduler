from typing import List
from fastapi import APIRouter, Depends
from db.database import get_db
from services.event_service import EventService
from db.schemas.event_schema import EventCreate, EventResponse

from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/events", tags=["Events"])

@router.post("/create", response_model=EventResponse)
async def create_event(event: EventCreate, db: AsyncSession = Depends(get_db)):
    """Create a new event."""
    return await EventService.create_event(event, db)

@router.get("/all", response_model=List[EventResponse])
async def get_all_events(db: AsyncSession = Depends(get_db)):
    """Fetch all events stored in the database."""
    return await EventService.get_all_events(db)

@router.get("/{id}", response_model=EventResponse)
async def get_event(id: int, db: AsyncSession = Depends(get_db)):
    """Fetch a specific event by ID."""
    return await EventService.get_event(id, db)

@router.put("/{id}", response_model=EventResponse)
async def update_event(id: int, updated_event: EventCreate, db: AsyncSession = Depends(get_db)):
    """Update an existing event."""
    return await EventService.update_event(id, updated_event, db)

@router.delete("/{id}")
async def delete_event(id: int, db: AsyncSession = Depends(get_db)):
    """Delete an event by ID."""
    return await EventService.delete_event(id, db)

@router.post("/trigger/{id}")
async def trigger_event(id: int, db: AsyncSession = Depends(get_db)):
    """Triggers an event and logs the response."""
    return await EventService.trigger_event(id, db)