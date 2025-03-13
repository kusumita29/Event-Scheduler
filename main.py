from fastapi import FastAPI

app = FastAPI()

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "OK", "message": "Service is running!"}
