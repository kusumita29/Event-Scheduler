from fastapi import APIRouter, Depends, HTTPException
from db.database import get_db
from services.log_service import LogService
from db.schemas.log_schema import LogResponse, LogsFilterByEventResponse
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/logs", tags=["Logs"])


@router.get("/", response_model=list[LogResponse])
async def get_all_logs(db: AsyncSession = Depends(get_db)) -> list[LogResponse]:
    """Retrieve all event logs."""
    return await LogService.get_all_logs(db)


@router.get("/filter/by/{event_id}")
async def get_logs_by_event(event_id: int, db: AsyncSession = Depends(get_db)) -> LogsFilterByEventResponse:
    """ API to fetch logs along with their count """
    logs_data = await LogService.get_logs_with_count(event_id, db)

    print ("kusumita", logs_data.model_dump)
    
    if logs_data.logs_count == 0:
        raise HTTPException(status_code=404, detail="No logs found for this event.")

    return logs_data