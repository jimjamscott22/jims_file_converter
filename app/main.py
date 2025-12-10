"""
Main FastAPI application entry point.
Sets up the web server, routes, and static file serving.
"""

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio

from app.config import settings
from app.api.routes import router
from app.services.file_handler import file_handler


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Handles startup and shutdown tasks.
    """
    # Startup
    print("🚀 Starting Jim's File Converter...")
    print(f"📁 Temp directory: {settings.temp_dir}")
    print(f"📊 Max file size: {settings.max_file_size_mb}MB")
    print(f"🔧 Supported formats: {', '.join(settings.supported_formats)}")
    
    # Start background task for cleanup
    cleanup_task = asyncio.create_task(periodic_cleanup())
    
    yield
    
    # Shutdown
    print("🛑 Shutting down...")
    cleanup_task.cancel()
    try:
        await cleanup_task
    except asyncio.CancelledError:
        pass


async def periodic_cleanup():
    """Background task to clean up old temporary files."""
    while True:
        try:
            await asyncio.sleep(3600)  # Run every hour
            await file_handler.cleanup_old_files(max_age_hours=2)
        except asyncio.CancelledError:
            break
        except Exception as e:
            print(f"Error in cleanup task: {e}")


# Create FastAPI application
app = FastAPI(
    title="Jim's File Converter",
    description="A web-based image conversion tool",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory=str(settings.static_dir)), name="static")

# Setup templates
templates = Jinja2Templates(directory=str(settings.templates_dir))

# Include API routes
app.include_router(router)


@app.get("/")
async def read_root(request: Request):
    """Serve the main page."""
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "max_file_size_mb": settings.max_file_size_mb,
            "supported_formats": settings.supported_formats
        }
    )


@app.get("/ping")
async def ping():
    """Simple ping endpoint for testing."""
    return {"message": "pong"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=True
    )

