from fastapi import FastAPI

from routes import events_router, logs_router, users_router

app = FastAPI()

app.include_router(events_router.router)
app.include_router(logs_router.router)
app.include_router(users_router.router)

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "OK", "message": "Service is running!"}
