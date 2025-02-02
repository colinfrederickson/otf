from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import auth_router, members_router, classes_router
from .core.config import settings
from .core.logging import logger

app = FastAPI(title="OTF API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(members_router)
app.include_router(classes_router)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

logger.info("Application startup complete")