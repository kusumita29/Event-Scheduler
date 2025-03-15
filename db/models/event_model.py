from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Enum, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from db.database import Base
from db.enums import EventType, MethodType

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)  # Auto-incremented primary key
    creator_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)  # Foreign key to users
    name = Column(String, nullable=False)
    event_type = Column(Enum(EventType), nullable=False)  # Uses predefined Enum
    destination = Column(String, nullable=False)
    method_type = Column(Enum(MethodType), nullable=False)  # Uses predefined Enum
    payload = Column(Text, nullable=True)  # Optional JSON payload
    is_test = Column(Boolean, default=False)

    created_at = Column(DateTime, server_default=func.now())  # Auto-generated timestamp
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())  # Updates on modification

    # Relationship with Logs and Users table
    logs = relationship("Log", back_populates="event")
    creator = relationship("User", back_populates="events")