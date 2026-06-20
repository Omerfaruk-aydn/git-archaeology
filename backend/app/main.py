from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import setup_logging
from app.middleware.error_handler import ErrorHandlerMiddleware
from app.api.v1.routes import repository, analysis, commits, reports, auth, providers

setup_logging()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Git depolarını analiz eden AI destekli araç",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(ErrorHandlerMiddleware)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(repository.router, prefix="/api/v1")
app.include_router(analysis.router, prefix="/api/v1")
app.include_router(commits.router, prefix="/api/v1")
app.include_router(reports.router, prefix="/api/v1")
app.include_router(providers.router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": settings.APP_VERSION}
