"""Coordinate transformation utilities for defect matching.

This module provides helpers for loading a similarity-transform configuration
and applying it to individual points or entire pandas DataFrames.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import math

import pandas as pd


@dataclass(frozen=True)
class TransformConfig:
    """Configuration for a 2D similarity transform.

    Attributes:
        scale: Multiplicative scale factor ``s``.
        rotation_deg: Rotation angle in degrees (counter-clockwise) ``θ``.
        tx_um: Translation along x in micrometers.
        ty_um: Translation along y in micrometers.
    """

    scale: float
    rotation_deg: float
    tx_um: float
    ty_um: float


def load_transform_config(path: str) -> TransformConfig:
    """Load a :class:`TransformConfig` from a JSON file.

    The JSON object must contain the keys ``scale``, ``rotation_deg``,
    ``tx_um``, and ``ty_um``.

    Args:
        path: Filesystem path to a JSON configuration file.

    Returns:
        Parsed transform configuration.

    Raises:
        FileNotFoundError: If ``path`` does not exist.
        json.JSONDecodeError: If the file is not valid JSON.
        KeyError: If any required field is missing.
        TypeError: If the JSON root is not an object.
        ValueError: If any field cannot be converted to ``float``.
    """

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, dict):
        raise TypeError("Transform config must be a JSON object.")

    return TransformConfig(
        scale=float(data["scale"]),
        rotation_deg=float(data["rotation_deg"]),
        tx_um=float(data["tx_um"]),
        ty_um=float(data["ty_um"]),
    )


def transform_xy(x_um: float, y_um: float, cfg: TransformConfig) -> tuple[float, float]:
    """Apply a similarity transform to a single point.

    The transform is:

    ``x' = s*(cosθ*x - sinθ*y) + tx``
    ``y' = s*(sinθ*x + cosθ*y) + ty``

    where ``θ`` is ``cfg.rotation_deg`` converted to radians.

    Args:
        x_um: Input x coordinate in micrometers.
        y_um: Input y coordinate in micrometers.
        cfg: Transform configuration.

    Returns:
        A tuple ``(x_ref_um, y_ref_um)`` containing transformed coordinates.
    """

    theta = math.radians(cfg.rotation_deg)
    cos_theta = math.cos(theta)
    sin_theta = math.sin(theta)

    x_ref_um = cfg.scale * (cos_theta * x_um - sin_theta * y_um) + cfg.tx_um
    y_ref_um = cfg.scale * (sin_theta * x_um + cos_theta * y_um) + cfg.ty_um
    return x_ref_um, y_ref_um


def transform_dataframe(a_df: pd.DataFrame, cfg: TransformConfig) -> pd.DataFrame:
    """Transform DataFrame coordinates and append reference columns.

    The input DataFrame must include columns ``x_um`` and ``y_um``. The output
    preserves all original columns and adds:

    - ``x_ref_um``
    - ``y_ref_um``

    Args:
        a_df: Source DataFrame containing ``x_um`` and ``y_um`` columns.
        cfg: Transform configuration.

    Returns:
        A new DataFrame with transformed coordinate columns appended.

    Raises:
        KeyError: If required input columns are missing.
    """

    required_columns = {"x_um", "y_um"}
    missing = required_columns.difference(a_df.columns)
    if missing:
        missing_str = ", ".join(sorted(missing))
        raise KeyError(f"Input DataFrame missing required columns: {missing_str}")

    theta = math.radians(cfg.rotation_deg)
    cos_theta = math.cos(theta)
    sin_theta = math.sin(theta)

    out_df = a_df.copy()
    out_df["x_ref_um"] = cfg.scale * (
        cos_theta * out_df["x_um"] - sin_theta * out_df["y_um"]
    ) + cfg.tx_um
    out_df["y_ref_um"] = cfg.scale * (
        sin_theta * out_df["x_um"] + cos_theta * out_df["y_um"]
    ) + cfg.ty_um
    return out_df
