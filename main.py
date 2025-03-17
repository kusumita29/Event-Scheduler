from typing import Any
from fastapi import FastAPI, Depends
from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_db

from routes import auth_router, events_router, logs_router, users_router

app = FastAPI()

app.include_router(auth_router.router)
app.include_router(users_router.router)
app.include_router(events_router.router)
app.include_router(logs_router.router)


# Health check endpoint
@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "OK", "message": "Service is running!"}

@app.get("/")
async def root(db: AsyncSession = Depends(get_db)) -> dict[str, Any | None]:
    result = await db.execute(text("SELECT 'Hello, Welcome to Event Scheduler!'"))
    message = result.scalar()
    return {"message": message}