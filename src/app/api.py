"""
API router for binding sub-routers.

Dependencies can be injected and passed down to specific sub-routers.
"""

from fastapi import APIRouter

from src.app.models import Predictor
from src.app.routes.predict import router as predict_router


def api_router(predictor: Predictor) -> APIRouter:
    api_router: APIRouter = APIRouter()

    @api_router.get("/health", include_in_schema=False)
    async def health_check() -> dict[str, str]:
        return {"status": "available"}

    @api_router.get("/")
    async def home() -> dict[str, str]:
        return {"message": "Hello 🐍 🚀 ✨"}

    api_router.include_router(
        predict_router(predictor), prefix="/predict", tags=["predict"]
    )

    return api_router
