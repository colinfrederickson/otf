from .auth import router as auth_router
from .members import router as members_router
from .classes import router as classes_router

__all__ = ["auth_router", "members_router", "classes_router"]