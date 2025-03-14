from pydantic import BaseModel, ConfigDict
from db.enums import EventType, MethodType
from datetime import datetime
from typing import Optional

class EventCreate(BaseModel):
    creator_id: int  # Foreign key (must be provided)
    name: str
    event_type: EventType
    destination: str
    method_type: MethodType
    payload: Optional[str] = None
    is_test: bool

# Response includes system-generated fields (id, created_at, updated_at)
class EventResponse(EventCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

