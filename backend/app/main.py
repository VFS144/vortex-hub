"""
Main FastAPI application - Production Ready (Local Environment Fix)
"""
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.core.database import Base, engine
from app.routes import auth, projects, tasks, bugs, lore

# Configure logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format=settings.LOG_FORMAT
)
logger = logging.getLogger(__name__)

# Create tables
Base.metadata.create_all(bind=engine)

# Disable docs in production
docs_url = None if settings.ENVIRONMENT == "production" else "/docs"
redoc_url = None if settings.ENVIRONMENT == "production" else "/redoc"
openapi_url = None if settings.ENVIRONMENT == "production" else "/openapi.json"

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Central operating system for Vortex Frame Studios",
    docs_url=docs_url,
    redoc_url=redoc_url,
    openapi_url=openapi_url,
)

# 1. GZip Compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# 2. Trusted Host - Adjusted for local dev to prevent connection refusal
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["*"] 
)

# 3. CORS middleware - Use configured origins from settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add security headers
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    # Note: HSTS requires HTTPS. Keeping for consistency, but won't affect local HTTP.
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response

# Exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    if settings.DEBUG:
        return JSONResponse(
            status_code=500,
            content={"detail": str(exc), "type": "DebugModeError"}
        )
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"}
    )

# Include routers
app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(tasks.router)
app.include_router(bugs.router)
app.include_router(lore.router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Vortex Hub",
        "tagline": "Every Frame. Infinite Impact.",
        "version": settings.APP_VERSION,
    }


@app.get("/health")
async def health():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
    }


@app.on_event("startup")
async def startup_event():
    """Run on app startup"""
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION} ({settings.ENVIRONMENT})")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on app shutdown"""
    logger.info(f"Shutting down {settings.APP_NAME}")


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )