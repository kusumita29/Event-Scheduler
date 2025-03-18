import asyncio
from db.database import init_db
from db.models.event_model import Event
from db.models.log_model import Log
from db.models.user_model import User


async def run_migration():
    await init_db()
    print("Tables created successfully!")


if __name__ == "__main__":
    asyncio.run(run_migration())
