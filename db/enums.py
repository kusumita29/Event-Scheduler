from enum import Enum

class UserRole(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    
class EventType(str, Enum):
    INTERVAL = "INTERVAL"  # Recurring events at a set interval
    FIXED_TIME = "FIXED_TIME"  # Events scheduled for a specific time
    ONE_TIME = "ONE_TIME"  # A single execution event


class MethodType(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


class LogStatus(str, Enum):
    ACTIVE = "ACTIVE"
    ARCHIVED = "ARCHIVED"
    DELETED = "DELETED"
