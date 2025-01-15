"""
Development entrypoint.
"""

import uvicorn

from src.common.configs import CONFIGS

if __name__ == "__main__":

    uvicorn.run(
        "src.main:app",
        workers=1,
        host=CONFIGS.HOST,
        port=int(CONFIGS.PORT),
        reload=True,  # Development only
        log_config=None,
    )
