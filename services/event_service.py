import requests
from datetime import datetime

from sqlalchemy import select
from db.schemas.event_schema import EventCreate, EventResponse
from db.enums import EventType, MethodType
from typing import List
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.events_model import Event
from db.schemas.log_schema import LogResponse
from services.log_service import LogService

class EventService:

    # Create an event
    @staticmethod
    async def create_event(event: EventCreate, db: AsyncSession) -> EventResponse:
        new_event = Event(
            creator_id=event.creator_id,
            name=event.name,
            event_type=event.event_type,
            destination=event.destination,
            method_type=event.method_type,
            payload=event.payload,
            is_test=event.is_test,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        db.add(new_event)
        await db.commit()
        await db.refresh(new_event)
        return EventResponse.from_orm(new_event)


    # Fetches all the events
    @staticmethod
    async def get_all_events(db: AsyncSession) -> List[EventResponse]:
        result = await db.execute(select(Event))
        events = result.scalars().all()
        return [EventResponse.from_orm(event) for event in events]
        

    # Fetches a single event by id
    @staticmethod
    async def get_event(event_id: int, db: AsyncSession) -> EventResponse:
        event = await db.get(Event, event_id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        return EventResponse.from_orm(event)


    # Update an event by id
    @staticmethod
    async def update_event(event_id: int, updated_event: EventCreate, db: AsyncSession) -> EventResponse:
        event = await db.get(Event, event_id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")

        event.name = updated_event.name
        event.event_type = updated_event.event_type
        event.destination = updated_event.destination
        event.method_type = updated_event.method_type
        event.payload = updated_event.payload
        event.is_test = updated_event.is_test
        event.updated_at = datetime.utcnow()

        await db.commit()
        await db.refresh(event)
        return EventResponse.from_orm(event)


    # Delete an event by id
    @staticmethod
    async def delete_event(event_id: int, db: AsyncSession) -> dict[str, str]:
        event = await db.get(Event, event_id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")

        await db.delete(event)
        await db.commit()
        return {"message": f"Event {event_id} deleted successfully"}
    

    @staticmethod
    async def trigger_event(event_id: int, db: AsyncSession) -> LogResponse:
        """
        Triggers an event by making an API request to its destination and logs the response.

        Args:
            event_id (int): The ID of the event to trigger.

        Returns:
            log_entry: Contains details of the API response of the event triggered.
        """

        # Retrieving the event details
        event = await db.get(Event, event_id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")

        method = event.method_type
        url = event.destination
        payload = event.payload

        response_text = "Request failed"
        response_status = 500  # Default to server error

        try:
            if method == MethodType.GET:
                response = requests.get(url)
            elif method == MethodType.POST:
                response = requests.post(url, json=payload)
            elif method == MethodType.PUT:
                response = requests.put(url, json=payload)
            elif method == MethodType.DELETE:
                response = requests.delete(url)
            else:
                raise HTTPException(status_code=400, detail="Unsupported method")

            # Update response details on success
            response_text = response.text
            response_status = response.status_code

        # Handling request failure (network issue, invalid URL, etc.)
        except requests.exceptions.RequestException as e:
            print(f"Exception occurred: {e}")
            response_text = str(e)

        # Logging the response
        log_entry = LogService.create_log(event_id, response_text, response_status)
        return log_entry