from fastapi import APIRouter
from services.log_service import LogService
from db.schemas.log_schema import LogResponse

router = APIRouter(prefix="/logs", tags=["Logs"])

@router.get("/", response_model=list[LogResponse])
def get_all_logs():
    """Retrieve all event logs."""
    return LogService.get_all_logs()