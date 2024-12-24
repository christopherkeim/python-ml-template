from typing import Any, Awaitable, Callable
from logging import Logger

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from src.logging.logger import LogSymbol


class StructuredHTTPRequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    This provides structured logging on all requests received by the
    FastAPI server and all responses it returns.
    """

    def __init__(
        self, app: ASGIApp, logger: Logger, symbols: LogSymbol = LogSymbol
    ) -> None:
        super().__init__(app)
        self.__logger = logger
        self.__symbols = symbols

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        to_log: dict[str, Any] = {
            "event": "request",
            "method": request.method,
            "url": str(request.url),
            "headers": dict(request.headers),
            "client": request.client.host,
        }
        self.__logger.info(f"Received REQUEST {to_log} {self.__symbols.REQUEST}")

        # Extract response body out of body iterator
        response = await call_next(request)
        response_body_builder: list[bytes] = []
        async for chunk in response.body_iterator:
            response_body_builder.append(chunk)

        response_body: bytes = b"".join(response_body_builder)
        to_log = {
            "event": "response",
            "status_code": response.status_code,
            "body": response_body.decode("utf-8"),
        }
        response_status_symbol = (
            self.__symbols.SUCCESS
            if response.status_code == 200
            else self.__symbols.ERROR
        )
        self.__logger.info(
            f"Sent RESPONSE {to_log} {self.__symbols.RESPONSE} {response_status_symbol}"
        )
        return Response(
            content=response_body,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type,
        )
