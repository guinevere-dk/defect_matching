from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

import pandas as pd


REQUIRED_A_COLUMNS = {"a_id", "x_a_um", "y_a_um"}
REQUIRED_B_COLUMNS = {"b_id", "x_ref_um", "y_ref_um"}


def read_csv_with_validation(path: str | Path, required_columns: set[str]) -> pd.DataFrame:
    """Read CSV and validate mandatory columns."""
    csv_path = Path(path)
    frame = pd.read_csv(csv_path)

    missing = required_columns - set(frame.columns)
    if missing:
        raise ValueError(f"{csv_path} is missing columns: {sorted(missing)}")

    return frame


def read_a_csv(path: str | Path) -> pd.DataFrame:
    return read_csv_with_validation(path, REQUIRED_A_COLUMNS)


def read_b_csv(path: str | Path) -> pd.DataFrame:
    return read_csv_with_validation(path, REQUIRED_B_COLUMNS)


def read_transform_config(path: str | Path) -> Dict[str, Any]:
    """Read JSON transform config."""
    config_path = Path(path)
    with config_path.open("r", encoding="utf-8") as file:
        config = json.load(file)

    required = {"scale_x", "scale_y", "rotation_deg", "offset_x", "offset_y"}
    missing = required - set(config.keys())
    if missing:
        raise ValueError(f"{config_path} is missing config keys: {sorted(missing)}")

    return config
