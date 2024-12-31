"""
These path definitions will execute every time you import a path into
a script.
"""

import os
from pathlib import Path

PARENT_DIR: Path = Path(__file__).parent.resolve().parent
MODELS_DIR: Path = PARENT_DIR / "models"


if not MODELS_DIR.exists():
    os.mkdir(MODELS_DIR)
