"""
Application entry point.
"""

import logging

from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from src.api import api_router
from src.exception_handlers import internal_server_error
from src.middleware import StructuredHTTPRequestLoggingMiddleware
from src.models import ModelProvider, ModelName, ModelSchema, Predictor
from src.rate_limiter import limiter
from src.common.configs import CONFIGS
from src.common.logs import init_logging
from src.model_providers.simple_model_provider.service import (
    build_simple_model_provider,
)
from src.predictors.simple_predictor.service import SimplePredictor


init_logging(level=CONFIGS.LOG_LEVEL, format=CONFIGS.LOG_FORMAT)
logger = logging.getLogger(__name__)

model_provider: ModelProvider = build_simple_model_provider()

predictor: Predictor = SimplePredictor(
    model_provider.get(ModelSchema(ModelName.MULTIPLIER))
)


app: FastAPI = FastAPI(openapi_url="")

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(StructuredHTTPRequestLoggingMiddleware)
app.add_middleware(GZipMiddleware, minimum_size=1000)

api: FastAPI = FastAPI(
    title="python-ml-template",
    description="A template web API for Python-based Machine Learning projects.",
    root_path="/api/v1",
    docs_url="/docs",
    openapi_url="/docs/openapi.json",
    # If you would like to use `redoc`
    # redoc_url="/docs", docs_url=None,
)

api.add_exception_handler(Exception, internal_server_error)

api.include_router(api_router(predictor))

app.mount("/api/v1", app=api)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.main:app",
        workers=1,
        host=CONFIGS.HOST,
        port=int(CONFIGS.PORT),
        reload=True,
        log_config=None,
    )
