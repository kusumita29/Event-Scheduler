from pydantic import BaseModel, ConfigDict, Field, model_validator
from db.enums import EventType, MethodType
from datetime import datetime, time
from typing import Optional

class EventCreate(BaseModel):
    name: str
    event_type: EventType
    destination: str
    method_type: MethodType
    payload: Optional[str] = None
    is_test: bool

    # Additional fields based on event type with default values
    interval_minutes: Optional[int] = Field(30, ge=1, description="Default trigger interval set to 30 minutes")
    fixed_time: Optional[time] = Field(time(9, 0), description="Daily trigger time set to 9 AM GMT")

    @model_validator(mode="before")
    @classmethod
    def validate_event_type(cls, values):
        event_type = getattr(values, "event_type", None)

        if event_type == EventType.INTERVAL:
            values.interval_minutes = values.interval_minutes or 30  # Default: 30 mins

        if event_type == EventType.FIXED_TIME:
            values.fixed_time = values.fixed_time or time(9, 0)  # Default: 9 AM

        return values

# Response includes system-generated fields (id, created_at, updated_at)
class EventResponse(EventCreate):
    id: int
    creator_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

