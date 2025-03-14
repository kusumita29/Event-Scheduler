import requests
from datetime import datetime
from db.schemas.event_schema import EventCreate, EventResponse
from db.enums import EventType, MethodType
from typing import List
from fastapi import HTTPException

from services.log_service import LogService

class EventService:
    # Initial hardcoded list of events
    events_db = [
        EventResponse(
            id=1,
            creator_id=101,
            name="System Backup",
            event_type=EventType.FIXED_TIME,
            destination="https://backup.example.com",
            method_type=MethodType.POST,
            payload='{"backup": "full"}',
            is_test=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        ),
        EventResponse(
            id=2,
            creator_id=102,
            name="Monthly Report",
            event_type=EventType.INTERVAL,
            destination="https://reports.example.com",
            method_type=MethodType.GET,
            payload=None,
            is_test=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        ),
        EventResponse(
            id=3,
            creator_id=103,
            name="User Signup Notification",
            event_type=EventType.ONE_TIME,
            destination="https://notify.example.com",
            method_type=MethodType.POST,
            payload='{"user_id": 1234, "email": "user@example.com"}',
            is_test=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
    ]

    event_id_counter = 4  # Start ID counter from 4

    @classmethod
    def create_event(cls, event: EventCreate) -> EventResponse:
        new_event = EventResponse(
            id=cls.event_id_counter,
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
        cls.events_db.append(new_event)
        cls.event_id_counter += 1
        return new_event

    @classmethod
    def get_all_events(cls) -> List[EventResponse]:
        return cls.events_db

    @classmethod
    def get_event(cls, id: int) -> EventResponse:
        for event in cls.events_db:
            if event.id == id:
                return event
        raise HTTPException(status_code=404, detail="Event not found")

    @classmethod
    def update_event(cls, id: int, updated_event: EventCreate) -> EventResponse:
        for event in cls.events_db:
            if event.id == id:
                event.name = updated_event.name
                event.event_type = updated_event.event_type
                event.destination = updated_event.destination
                event.method_type = updated_event.method_type
                event.payload = updated_event.payload
                event.is_test = updated_event.is_test
                event.updated_at = datetime.utcnow()
                return event
        raise HTTPException(status_code=404, detail="Event not found")

    @classmethod
    def delete_event(cls, id: int) -> dict:
        for event in cls.events_db:
            if event.id == id:
                cls.events_db.remove(event)
                return {"message": f"Event {id} deleted successfully"}
        raise HTTPException(status_code=404, detail="Event not found")
    
    @classmethod
    def trigger_event(cls, event_id: int):
        """
        Triggers an event by making an API request to its destination and logs the response.

        Args:
            event_id (int): The ID of the event to trigger.

        Returns:
            log_entry: Contains details of the API response of the event triggered.
        """

        # Retrieve the event details
        event = cls.get_event(event_id)
        if not event:
            return {"error": "Event not found"}, 404

        method = event.method_type  # HTTP method 
        url = event.destination  # Target URL
        payload = event.payload  # Request payload (if applicable)

        # Default response values in case of failure
        response_text = "Request failed"
        response_status = 500  # Internal Server Error

        try:
            # Make an HTTP request based on the method type
            if method == "GET":
                response = requests.get(url)
            elif method == "POST":
                response = requests.post(url, json=payload)
            elif method == "PUT":
                response = requests.put(url, json=payload)
            elif method == "DELETE":
                response = requests.delete(url)
            else:
                return {"error": "Unsupported HTTP method"}, 400  # Bad Request

            # Update response details on success
            response_text = response.text
            response_status = response.status_code

        except requests.exceptions.RequestException as e:
            # Handle request failure (network issue, invalid URL, etc.)
            print(f"Exception occurred: {e}")
            response_text = str(e)

        # Log the request outcome (success or failure)
        log_entry = LogService.create_log(event_id, response_text, response_status)

        return log_entry  # Return log entry with HTTP 200 (OK)

        