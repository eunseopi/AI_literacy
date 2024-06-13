from .llm import llm_router
from .login import login_router
from .score_dashboard import score_dashboard_router
from .register import register_router
from .profile import profile_router


__all__ = [
    "llm_router",
    "login_router",
    "score_dashboard_router",
    "register_router",
    "profile_router",
]
