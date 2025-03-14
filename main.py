from fastapi import FastAPI

from routes import events, logs

app = FastAPI()

app.include_router(events.router)
app.include_router(logs.router)

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "OK", "message": "Service is running!"}
