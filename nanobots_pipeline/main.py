from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
from api.routes import router
from scheduler.cron_jobs import start_scheduler
import logging

logging.basicConfig(level=logging.INFO)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize background services on startup."""
    start_scheduler()
    logging.info("NanoBots Pipeline Backend Started Successfully.")
    yield
    logging.info("NanoBots Pipeline Backend Shutting Down.")

app = FastAPI(
    title="NanoBots Agent Pipeline",
    description="Enterprise-Grade NanoBot Agent Pipeline with Clean Architecture",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(router, prefix="/api/v1")

# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", include_in_schema=False)
async def serve_frontend():
    """Serves the beautiful dark theme UI client."""
    return FileResponse("static/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
