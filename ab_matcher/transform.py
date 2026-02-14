from __future__ import annotations

import math

import pandas as pd


def transform_a_to_reference(a_df: pd.DataFrame, config: dict) -> pd.DataFrame:
    """Transform A coordinates into reference coordinates.

    Transform order: scale -> rotate -> translate.
    """
    scale_x = float(config["scale_x"])
    scale_y = float(config["scale_y"])
    rotation_deg = float(config["rotation_deg"])
    offset_x = float(config["offset_x"])
    offset_y = float(config["offset_y"])

    theta = math.radians(rotation_deg)
    cos_t = math.cos(theta)
    sin_t = math.sin(theta)

    x_scaled = a_df["x_a_um"].to_numpy(dtype=float) * scale_x
    y_scaled = a_df["y_a_um"].to_numpy(dtype=float) * scale_y

    x_rot = x_scaled * cos_t - y_scaled * sin_t
    y_rot = x_scaled * sin_t + y_scaled * cos_t

    out = a_df.copy()
    out["x_ref_um"] = x_rot + offset_x
    out["y_ref_um"] = y_rot + offset_y
    return out
