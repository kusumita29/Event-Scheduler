import asyncio
from db.database import init_db
from models.events_model import Event

async def run_migration():
    await init_db()
    print("Tables created successfully!")

if __name__ == "__main__":
    asyncio.run(run_migration())
