"""
Logging configuration.

Handlers are set to a default level of "INFO".

The root logger level is configurable via a "LOG_LEVEL" environment variable.

A rotating file handler can be added if desired:

"handlers": {
    "default": {},
    "stream_handler": {},
    "file_handler": {
        "formatter": "json_formatter",
        "level": "INFO",
        "class": "logging.handlers.RotatingFileHandler",
        "filename": "app.log",
        "maxBytes": 1024 * 1024 * 1,  # = 1MB
        "backupCount": 3,
    },
}
"""

from typing import Literal
from logging import config, getLogger, Logger

STANDARD_FORMATTER: str = (
    "[%(asctime)s] [%(process)d::%(threadName)s] [%(filename)s::%(lineno)d] [%(name)s] [%(levelname)s] %(message)s"
)

JSON_FORMATTER: str = (
    "{'time': '%(asctime)s', 'process': '%(process)d', 'thread_name': '%(threadName)s', 'thread_id': '%(thread)s', 'level': '%(levelname)s', 'logger_name': '%(name)s', 'message': '%(message)s'}"
)

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    # Global log formatting.
    "formatters": {
        "global_formatter": {"format": JSON_FORMATTER},
    },
    "handlers": {
        "default": {
            "formatter": "global_formatter",
            "level": "INFO",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",  # Default is stderr
        },
        "stream_handler": {
            "formatter": "global_formatter",
            "level": "INFO",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",  # Default is stderr
        },
    },
    "loggers": {
        "": {
            "handlers": ["stream_handler"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn": {
            "handlers": ["stream_handler"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.access": {
            "handlers": ["stream_handler"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.error": {
            "handlers": ["stream_handler"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.asgi": {
            "handlers": ["stream_handler"],
            "level": "INFO",
            "propagate": False,
        },
    },
}


def new_logger(
    name: str, level: str = "INFO", format: Literal["standard", "json"] = "json"
) -> Logger:

    LOGGING_CONFIG["loggers"][""]["level"] = level

    if format != "json":
        LOGGING_CONFIG["formatters"]["global_formatter"]["format"] = STANDARD_FORMATTER

    config.dictConfig(LOGGING_CONFIG)

    return getLogger(name)
