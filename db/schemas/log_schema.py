from datetime import datetime

from pydantic import BaseModel, ConfigDict

from db.enums import LogStatus

class LogCreate(BaseModel):
    event_id: int  # Foreign key (must be provided)
    response: str
    response_status_code: int
    status: LogStatus

# Response includes system-generated fields (id, timestamp)
class LogResponse(LogCreate):
    id: int  # System-generated ID
    timestamp: datetime  # Auto-generated

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)
