from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db
from db.models.user_model import User
from db.schemas.event_schema import EventCreate, EventResponse
from db.schemas.log_schema import LogResponse
from services.auth_service import AuthService
from services.event_service import EventService

router = APIRouter(prefix="/events", tags=["Events"])


@router.post("/create", response_model=EventResponse)
async def create_event(
    event: EventCreate,
    current_user: User = Depends(AuthService.get_current_user),
    db: AsyncSession = Depends(get_db),
) -> EventResponse:
    """Create an event"""

    return await EventService.create_event(current_user.id, event, db)


@router.get("/all", response_model=List[EventResponse])
async def get_all_events(
    current_user: User = Depends(AuthService.get_current_user),
    db: AsyncSession = Depends(get_db),
) -> List[EventResponse]:
    """Fetch all your created events."""

    return await EventService.get_all_events(current_user.id, db)


@router.get("/{id}", response_model=EventResponse)
async def get_event(
    id: int,
    current_user: User = Depends(AuthService.get_current_user),
    db: AsyncSession = Depends(get_db),
) -> EventResponse:
    """Fetch a specific event by ID."""

    return await EventService.get_event(id, current_user.id, db)


@router.put("/{id}", response_model=EventResponse)
async def update_event(
    id: int,
    updated_event: EventCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user),
) -> EventResponse:
    """Update an existing event."""

    return await EventService.update_event(id, current_user.id, updated_event, db)


@router.delete("/{id}")
async def delete_event(
    id: int,
    current_user: User = Depends(AuthService.get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete an event by ID."""

    return await EventService.delete_event(id, current_user.id, db)


@router.post("/trigger/{id}")
async def trigger_event(
    id: int,
    current_user: User = Depends(AuthService.get_current_user),
    db: AsyncSession = Depends(get_db),
) -> LogResponse:
    """Triggers an event and logs the response."""

    return await EventService.trigger_event(id, current_user.id, db)
