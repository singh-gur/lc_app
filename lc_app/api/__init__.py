# create a fastapi app
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter

def create_app() -> FastAPI:
    """Create a FastAPI application."""
    app = FastAPI(
        title="LangChain App",
        description="LangChain App API",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include the API router
    api_router = APIRouter()
    app.include_router(api_router, prefix="/api")

    # Serve static files
    app.mount("/static", StaticFiles(directory="static"), name="static")

    return app