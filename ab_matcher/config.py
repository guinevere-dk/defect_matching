from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_json_config(path: str) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as fp:
        return json.load(fp)
