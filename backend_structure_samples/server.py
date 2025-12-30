"""
Production-Ready FastAPI Server
Enhanced with best practices for production deployment
"""
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
import logging
import sys
from pathlib import Path

# Import configuration
from config import get_settings

# Import middleware
from middleware import (
    RequestIDMiddleware,
    RequestLoggingMiddleware,
    RateLimitMiddleware,
    SecurityHeadersMiddleware,
    ProxyHeaderMiddleware,
)

# Import custom exceptions
from exceptions import BaseAPIException

# Import database
from database import close_db_connection, db

# Import routes (with versioning)
from routes.v1 import (
    auth_router,
    client_auth_router,
    projects_router,
    services_router,
    blogs_router,
    testimonials_router,
    contacts_router,
    bookings_router,
    booking_settings_router,
    admins_router,
    admin_clients_router,
    admin_client_projects_router,
    client_projects_router,
    analytics_router,
    newsletter_router,
    pricing_router,
    storage_router,
    skills_router,
    pages_router,
    about_router,
    contact_page_router,
    chat_router,
    notes_router,
    content_router,
    settings_router,
    credentials_router,
    health_router,
)

# Get settings
settings = get_settings()

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Backend API for MSPN DEV website and admin panel",
    version=settings.APP_VERSION,
    docs_url="/api/docs" if settings.DEBUG else None,  # Disable in production
    redoc_url="/api/redoc" if settings.DEBUG else None,
    openapi_url="/api/openapi.json" if settings.DEBUG else None,
    root_path="/api" if settings.TRUST_PROXY else "",
)

# ============================================================================
# MIDDLEWARE SETUP (Order matters!)
# ============================================================================

# 1. Proxy headers (must be first)
app.add_middleware(ProxyHeaderMiddleware)

# 2. Security headers
app.add_middleware(SecurityHeadersMiddleware)

# 3. CORS
cors_origins = settings.parse_cors_origins()
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. GZip compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# 5. Rate limiting
if settings.RATE_LIMIT_ENABLED:
    app.add_middleware(
        RateLimitMiddleware,
        requests_per_minute=settings.RATE_LIMIT_PER_MINUTE
    )

# 6. Request ID
app.add_middleware(RequestIDMiddleware)

# 7. Request logging
app.add_middleware(RequestLoggingMiddleware)

# ============================================================================
# EXCEPTION HANDLERS
# ============================================================================

@app.exception_handler(BaseAPIException)
async def custom_exception_handler(request: Request, exc: BaseAPIException):
    """Handle custom API exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors with better formatting"""
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(x) for x in error["loc"]),
            "message": error["msg"],
            "type": error["type"],
        })
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Validation error",
            "errors": errors
        }
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle all uncaught exceptions"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error" if not settings.DEBUG else str(exc)
        }
    )

# ============================================================================
# HEALTH CHECK ENDPOINTS
# ============================================================================

@app.get("/", tags=["Health"])
async def root_health_check():
    """Root health check endpoint"""
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Detailed health check with database status"""
    try:
        # Check database connection
        await db.command("ping")
        db_status = "healthy"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        db_status = "unhealthy"
    
    return {
        "status": "healthy" if db_status == "healthy" else "degraded",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "checks": {
            "database": db_status,
        }
    }

# ============================================================================
# API ROUTES (Version 1)
# ============================================================================

# Create versioned API router
from fastapi import APIRouter
api_v1 = APIRouter(prefix="/api/v1")

# Include all routers
api_v1.include_router(auth_router)
api_v1.include_router(client_auth_router)
api_v1.include_router(projects_router)
api_v1.include_router(services_router)
api_v1.include_router(blogs_router)
api_v1.include_router(testimonials_router)
api_v1.include_router(contacts_router)
api_v1.include_router(bookings_router)
api_v1.include_router(booking_settings_router)
api_v1.include_router(admins_router)
api_v1.include_router(admin_clients_router)
api_v1.include_router(admin_client_projects_router)
api_v1.include_router(client_projects_router)
api_v1.include_router(analytics_router)
api_v1.include_router(newsletter_router)
api_v1.include_router(pricing_router)
api_v1.include_router(storage_router)
api_v1.include_router(skills_router)
api_v1.include_router(pages_router)
api_v1.include_router(about_router)
api_v1.include_router(contact_page_router)
api_v1.include_router(chat_router)
api_v1.include_router(notes_router)
api_v1.include_router(content_router)
api_v1.include_router(settings_router)
api_v1.include_router(credentials_router)
api_v1.include_router(health_router)

# Include versioned router in main app
app.include_router(api_v1)

# Legacy /api prefix for backward compatibility
legacy_api = APIRouter(prefix="/api")
legacy_api.include_router(auth_router)
legacy_api.include_router(client_auth_router)
legacy_api.include_router(projects_router)
legacy_api.include_router(services_router)
legacy_api.include_router(blogs_router)
legacy_api.include_router(testimonials_router)
legacy_api.include_router(contacts_router)
legacy_api.include_router(bookings_router)
legacy_api.include_router(booking_settings_router)
legacy_api.include_router(admins_router)
legacy_api.include_router(admin_clients_router)
legacy_api.include_router(admin_client_projects_router)
legacy_api.include_router(client_projects_router)
legacy_api.include_router(analytics_router)
legacy_api.include_router(newsletter_router)
legacy_api.include_router(pricing_router)
legacy_api.include_router(storage_router)
legacy_api.include_router(skills_router)
legacy_api.include_router(pages_router)
legacy_api.include_router(about_router)
legacy_api.include_router(contact_page_router)
legacy_api.include_router(chat_router)
legacy_api.include_router(notes_router)
legacy_api.include_router(content_router)
legacy_api.include_router(settings_router)
legacy_api.include_router(credentials_router)

app.include_router(legacy_api)

# ============================================================================
# STARTUP & SHUTDOWN EVENTS
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    logger.info(f"🚀 Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"📝 Environment: {settings.ENVIRONMENT}")
    logger.info(f"🔗 Database: {settings.DB_NAME}")
    logger.info(f"🌐 CORS Origins: {cors_origins}")
    
    # Run auto-initialization
    try:
        from auto_init import auto_initialize_database
        await auto_initialize_database()
        logger.info("✅ Auto-initialization complete")
    except Exception as e:
        logger.error(f"❌ Auto-initialization failed: {e}")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("🛑 Shutting down application")
    await close_db_connection()
    logger.info("✅ Shutdown complete")


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "server:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        workers=1 if settings.DEBUG else settings.WORKERS,
        log_level=settings.LOG_LEVEL.lower(),
    )
