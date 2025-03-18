from sqlalchemy import Column, ForeignKey, Integer, String, Enum, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from db.database import Base
from db.enums import LogStatus


class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    event_id = Column(
        Integer, ForeignKey("events.id", ondelete="CASCADE")
    )  # Foreign key to Event
    response = Column(String, nullable=False)  # Stores response text
    response_status_code = Column(Integer, nullable=False)  # HTTP response status
    timestamp = Column(DateTime, default=datetime.utcnow)  # Auto-generated timestamp
    status = Column(
        Enum(LogStatus), nullable=False, default=LogStatus.ACTIVE
    )  # Log status

    # Relation with event
    event = relationship("Event", back_populates="logs")
