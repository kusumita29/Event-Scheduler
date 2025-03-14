from datetime import datetime
from db.enums import LogStatus
from db.schemas.log_schema import logResponse

class LogService:
    logs_db = []  # Static list for now
    log_id_counter = 1

    @classmethod
    def create_log(cls, event_id: int, response: str, response_status_code: int):
        """Creates a log entry and stores it."""
        log_entry = {
            "id": cls.log_id_counter,
            "event_id": event_id,
            "response": response,
            "response_status_code": response_status_code,
            "timestamp": datetime.utcnow(),
            "status": LogStatus.ACTIVE  # Default status
        }
        cls.logs_db.append(log_entry)
        cls.log_id_counter += 1
        print("Logs in DB:", cls.logs_db)  
        return log_entry
    
    @classmethod
    def get_all_logs(cls) -> list[logResponse]:
        return cls.logs_db
