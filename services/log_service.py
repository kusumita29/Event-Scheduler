from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from db.enums import LogStatus
from db.models.event_model import Event
from db.models.log_model import Log
from db.schemas.log_schema import LogResponse, LogsFilterByEventResponse


class LogService:

    @staticmethod
    async def create_log(
        event_id: int, response_text: str, response_status: int, db: AsyncSession
    ) -> LogResponse:
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
            raise HTTPException(
                status_code=500, detail=f"Failed to store log: {str(e)}"
            )

    @staticmethod
    async def get_all_logs(user_id: int, db: AsyncSession) -> list[LogResponse]:
        """Fetch all logs for the events you created."""

        result = await db.execute(
            select(Log)
            .join(Event, Event.id == Log.event_id)
            .where(Event.creator_id == user_id)
            .options(joinedload(Log.event))
        )

        logs = result.scalars().all()

        if not logs:
            raise HTTPException(status_code=404, detail="No logs found for this user.")

        return [LogResponse.model_validate(log) for log in logs]

    @staticmethod
    async def get_logs_with_count(
        user_id: int, event_id: int, db: AsyncSession
    ) -> LogsFilterByEventResponse:
        """Fetch logs for an event along with their count."""

        # Checks if event is created by the user
        event_exists = await db.execute(
            select(Event.id).where(Event.id == event_id, Event.creator_id == user_id)
        )
        if not event_exists.scalar():
            raise HTTPException(
                status_code=403, detail="You do not have access to this event."
            )

        # Fetch logs for the given event_id
        logs_result = await db.execute(select(Log).where(Log.event_id == event_id))
        logs = logs_result.scalars().all()

        return LogsFilterByEventResponse(
            event_id=event_id,
            logs_count=len(logs),
            logs=[LogResponse.model_validate(log) for log in logs],  # Convert to schema
        )
