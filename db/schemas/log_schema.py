from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict

from db.enums import LogStatus    

# Response includes system-generated fields (id, timestamp)
class LogResponse(BaseModel):
    id: int  # System-generated ID
    event_id: int  # Foreign key (must be provided)
    response: str
    response_status_code: int
    timestamp: datetime  # Auto-generated
    status: LogStatus

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

class LogsFilterByEventResponse(BaseModel):
    event_id: int
    logs_count: int
    logs: List[LogResponse]

    class Config:
        from_attributes = True