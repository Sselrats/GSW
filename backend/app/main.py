from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.sessions import SessionMiddleware
from typing import Dict, Any
import uvicorn
import os
import asyncio

from app.core.config import settings
from app.api.endpoints import gsw as gsw_endpoints
from app.services.gsw_service import GSWService

# Create an instance for session cleanup
gsw_service_instance = GSWService()

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="GSW Encryption Service API",
    version=settings.VERSION,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Add session middleware
app.add_middleware(
    SessionMiddleware,
    secret_key="your-secure-secret-key",  # In production, use a secure secret from environment variables
    session_cookie="gsw_session",
    max_age=3600  # 1 hour
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(
    gsw_endpoints.router,
    prefix="/api/v1/gsw",
    tags=["gsw"]
)

# Session cleanup task
async def cleanup_sessions_periodically():
    """Periodically clean up expired sessions."""
    while True:
        await asyncio.sleep(3600)  # Run every hour
        gsw_service_instance._cleanup_sessions()

@app.on_event("startup")
async def startup_event():
    """Startup event handler to initialize background tasks."""
    # Start the session cleanup task
    asyncio.create_task(cleanup_sessions_periodically())

@app.get("/api/health", response_model=Dict[str, str])
async def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "message": str(exc.detail)},
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"success": False, "message": "An unexpected error occurred"},
    )

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info" if settings.DEBUG else "warning"
    )