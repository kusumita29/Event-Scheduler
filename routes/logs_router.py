from fastapi import APIRouter, Depends
from db.database import get_db
from services.log_service import LogService
from db.schemas.log_schema import LogResponse
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/logs", tags=["Logs"])

@router.get("/", response_model=list[LogResponse])
async def get_all_logs(db: AsyncSession = Depends(get_db)):
    """Retrieve all event logs."""
    return await LogService.get_all_logs(db)