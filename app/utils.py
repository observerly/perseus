import os
from pathlib import Path


def get_root() -> Path:
    return Path(os.path.abspath(__file__)).absolute().parent.parent


ROOT_DIR = get_root()
