from typing import Callable
import logging

from src.app.models import (
    Input,
    ModelArtefact,
    Prediction,
    Predictor,
)


logger = logging.getLogger(__name__)


class SimplePredictor(Predictor):
    def __init__(self, model_artefact: ModelArtefact) -> None:
        self.__multiplier = self.__load(model_artefact)

    def predict(self, input: Input) -> Prediction:
        logger.info(f"running prediction on x={input.x} y={input.y}")

        return Prediction(
            model="simple_predictor", prediction=self.__multiplier(input.x, input.y)
        )

    def __load(self, model_artefact: ModelArtefact) -> Callable:
        logger.info(
            f"loading {model_artefact.model_schema.name} from {model_artefact.uri}"
        )
        return lambda x, y: x * y
