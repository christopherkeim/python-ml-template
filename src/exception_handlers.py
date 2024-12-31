import logging
import traceback as tb

from fastapi import Request, status
from fastapi.responses import JSONResponse


logger = logging.getLogger(__name__)


async def internal_server_error(request: Request, exception: Exception) -> JSONResponse:
    logger.error("".join(tb.format_exception(exception)))

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": [
                {"msg": "Internal Server Error", "loc": ["Unknown"], "type": "Unknown"}
            ]
        },
    )
