"""
Bases, mixins, interfaces, Pydantic models, and SQLAlchemy models.

Can be extended to a package for more complex software.
"""

from __future__ import annotations
from typing import Protocol
from dataclasses import dataclass
from enum import Enum

from pydantic import BaseModel


class Input(BaseModel):
    x: float
    y: float


class Prediction(BaseModel):
    model: str
    prediction: float


class Predictor(Protocol):
    """
    Predictor interface.
    """

    def predict(self, input: Input) -> Prediction: ...


class ModelName(str, Enum):
    MULTIPLIER = "multiplier"

    def __str__(self) -> str:
        return self.value


@dataclass
class ModelSchema:
    name: ModelName
    version: str | None = None

    def slug(self) -> str:
        """Discretion of model naming schema."""
        return f"{self.name}{('_' + self.version) if self.version else ''}"


@dataclass
class ModelArtefact:
    model_schema: ModelSchema
    uri: str


class ModelProvider(Protocol):
    """
    An abstraction over model registries that provides verified
    URIs to on-disk ML/DL model artefacts.

    Model registry URI should be injected via environment variables
    (whether the registry is local or over network).

    The details of mapping a schema to a disk artefact are the
    responsibility of the specific provider and model naming
    schema.
    """

    def get(self, model: ModelSchema) -> ModelArtefact: ...
    def __download_models(self) -> None:
        """
        Downloads a set of model artefacts to disk if they do not exist locally.

        This function should be run on initialization and raise on failure.
        """
        ...

    def list(self) -> list[ModelArtefact]: ...
