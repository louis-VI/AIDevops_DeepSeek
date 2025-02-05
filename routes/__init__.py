# routes/__init__.py
from .chat_routes import router as chat_router
from .code_routes import router as code_router
from .download_routes import router as download_router

# 导出所有路由
__all__ = ["chat_router", "code_router", "download_router"]