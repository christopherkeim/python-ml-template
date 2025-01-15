"""
Entrypoint.
"""

import uvicorn

from src.common.configs import CONFIGS

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.main:app",
        workers=1,
        host=CONFIGS.HOST,
        port=int(CONFIGS.PORT),
        log_config=None,
    )
