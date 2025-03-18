from datetime import datetime
from typing import List

import httpx
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.enums import EventType, MethodType
from db.models.event_model import Event
from db.schemas.event_schema import EventCreate, EventResponse
from db.schemas.log_schema import LogResponse
from services.log_service import LogService


class EventService:

    @staticmethod
    async def create_event(
        user_id: int, event: EventCreate, db: AsyncSession
    ) -> EventResponse:
        """Create an event and stores it in the database."""

        new_event = Event(
            creator_id=user_id,
            name=event.name,
            event_type=event.event_type,
            destination=event.destination,
            method_type=event.method_type,
            payload=event.payload,
            is_test=event.is_test,
            interval_minutes=(
                event.interval_minutes
                if event.event_type == EventType.INTERVAL
                else None
            ),
            fixed_time=(
                event.fixed_time if event.event_type == EventType.FIXED_TIME else None
            ),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        db.add(new_event)
        await db.commit()
        await db.refresh(new_event)
        return EventResponse.model_validate(new_event)

    @staticmethod
    async def get_all_events(user_id: int, db: AsyncSession) -> List[EventResponse]:
        """Get all events in the database."""

        result = await db.execute(select(Event).where(Event.creator_id == user_id))
        events = result.scalars().all()
        return [EventResponse.model_validate(event) for event in events]

    @staticmethod
    async def get_event(event_id: int, user_id: int, db: AsyncSession) -> EventResponse:
        """Fetches an event by id"""

        event = await db.get(Event, event_id)

        if not event:
            raise HTTPException(status_code=404, detail="Event not found")

        if event.creator_id != user_id:
            raise HTTPException(
                status_code=401, detail="You can only view your created events!"
            )

        return EventResponse.model_validate(event)

    @staticmethod
    async def update_event(
        event_id: int, user_id: int, updated_event: EventCreate, db: AsyncSession
    ) -> EventResponse:
        """Update an event by id"""
        event = await db.get(Event, event_id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")

        if event.creator_id != user_id:
            raise HTTPException(
                status_code=403, detail="You are not authorized to update this event"
            )

        event.name = updated_event.name
        event.event_type = updated_event.event_type
        event.destination = updated_event.destination
        event.method_type = updated_event.method_type
        event.payload = updated_event.payload
        event.is_test = updated_event.is_test
        event.interval_minutes = (
            updated_event.interval_minutes
            if updated_event.event_type == EventType.INTERVAL
            else None
        )
        event.fixed_time = (
            updated_event.fixed_time
            if updated_event.event_type == EventType.FIXED_TIME
            else None
        )
        event.updated_at = datetime.utcnow()

        await db.commit()
        await db.refresh(event)
        return EventResponse.model_validate(event)

    @staticmethod
    async def delete_event(
        event_id: int, user_id: int, db: AsyncSession
    ) -> dict[str, str]:
        """Delete an event by id"""
        event = await db.get(Event, event_id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")

        if event.creator_id != user_id:
            raise HTTPException(
                status_code=403, detail="You are not authorized to delete this event"
            )

        await db.delete(event)
        await db.commit()
        return {"message": f"Event {event_id} deleted successfully"}

    @staticmethod
    async def trigger_event(
        event_id: int, user_id: int, db: AsyncSession
    ) -> LogResponse:
        """
        Triggers an event by making an API request to its destination and logs the response.

        Args:
            event_id (int): The ID of the event to trigger.
            db (AsyncSession): The database session.

        Returns:
            LogResponse: Contains details of the API response of the event triggered.
        """
        # Retrieving the event details
        event = await db.get(Event, event_id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")

        if event.creator_id != user_id:
            raise HTTPException(
                status_code=403, detail="You can only trigger your created events"
            )

        method = event.method_type
        url = event.destination
        payload = event.payload

        response_text = "Request failed"
        response_status = 500  # Default to server error

        async with httpx.AsyncClient() as client:
            try:
                if method == MethodType.GET:
                    response = await client.get(url)
                elif method == MethodType.POST:
                    response = await client.post(url, json=payload)
                elif method == MethodType.PUT:
                    response = await client.put(url, json=payload)
                elif method == MethodType.DELETE:
                    response = await client.delete(url)
                else:
                    raise HTTPException(status_code=400, detail="Unsupported method")

                # Update response details on success
                response_text = response.text
                response_status = response.status_code

            # Handling request failure (network issue, invalid URL, etc.)
            except httpx.RequestError as e:
                print(f"Exception occurred: {e}")
                response_text = str(e)

        # Logging the response
        log_entry = await LogService.create_log(
            event_id, response_text, response_status, db
        )
        return log_entry
