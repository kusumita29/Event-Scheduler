from sqlalchemy import Column, Enum, Integer, String
from db.database import Base
from sqlalchemy.orm import relationship
from db.enums import UserRole


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)  # Auto-incremented primary key
    user_name = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)  # Uses predefined Enum

    # Relationship with Events
    events = relationship("Event", back_populates="creator", cascade="all, delete-orphan")
