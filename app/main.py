"""
Main application file for Background Remover API.
This is the entry point of the FastAPI application.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import remove_bg


# Create the FastAPI application instance
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description=settings.API_DESCRIPTION,
    docs_url="/docs",  # Swagger UI documentation
    redoc_url="/redoc"  # ReDoc documentation
)


# Configure CORS (Cross-Origin Resource Sharing)
# This allows the API to be called from web browsers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact domains
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


# Include routers
# This connects our endpoint routes to the main app
app.include_router(remove_bg.router)


@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint - provides basic API information.
    Visit this URL to see if the API is running.
    """
    return {
        "message": "Welcome to Background Remover API",
        "version": settings.API_VERSION,
        "docs": "/docs",
        "health": "/api/health",
        "endpoints": {
            "remove_background": "POST /api/remove-bg"
        }
    }


# This block runs when you execute: python -m app.main
if __name__ == "__main__":
    import uvicorn
    
    print(f"🚀 Starting {settings.API_TITLE}")
    print(f"📍 Server: http://{settings.HOST}:{settings.PORT}")
    print(f"📚 Docs: http://{settings.HOST}:{settings.PORT}/docs")
    
    # Start the server
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True  # Auto-reload on code changes (disable in production)
    )