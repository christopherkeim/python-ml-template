"""
/predict
"""

from fastapi import APIRouter

from src.app.models import Input, Prediction, Predictor


def router(predictor: Predictor) -> APIRouter:
    router: APIRouter = APIRouter()

    @router.get("", response_model=Prediction)
    def get_prediction(x: float, y: float):
        return predictor.predict(input=Input(x=x, y=y))

    return router
