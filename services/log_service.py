from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import func
from db.enums import LogStatus
from db.schemas.log_schema import LogResponse, LogsWithCountResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime
from db.models.log_model import Log

class LogService:

    @staticmethod
    async def create_log(event_id: int, response_text: str, response_status: int, db: AsyncSession) -> LogResponse:
        """Creates a log entry and stores it in the database."""
        new_log = Log(
            event_id=event_id,
            response=response_text,
            response_status_code=response_status,
            timestamp=datetime.utcnow(),
            status=LogStatus.ACTIVE,  # Default status
        )

        try:
            db.add(new_log)
            await db.commit()
            await db.refresh(new_log)
            return LogResponse.model_validate(new_log)
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500, detail=f"Failed to store log: {str(e)}")
    
    
    @staticmethod
    async def get_all_logs(db: AsyncSession) -> list[LogResponse]:
        """Fetch all logs from the database."""
        result = await db.execute(select(Log))
        logs = result.scalars().all()
        return [LogResponse.model_validate(log) for log in logs]


    @staticmethod
    async def get_logs_with_count(event_id: int, db: AsyncSession) -> LogsWithCountResponse:
        """Fetch logs for an event along with their count."""
        
        # Fetch logs for the given event_id
        logs_result = await db.execute(select(Log).where(Log.event_id == event_id))
        logs = logs_result.scalars().all()

        return LogsWithCountResponse(
            event_id=event_id,
            logs_count=len(logs),
            logs=[LogResponse.model_validate(log) for log in logs]  # Convert to schema
        )
