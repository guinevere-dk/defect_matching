from __future__ import annotations

from typing import Iterable


def transform_points(points: Iterable[tuple[float, float]], config: dict) -> list[tuple[float, float]]:
    """Apply scale -> rotate -> translate transform to 2D points."""
    scale = float(config.get("scale", 1.0))
    theta_deg = float(config.get("rotation_deg", 0.0))
    tx, ty = config.get("translation", (0.0, 0.0))

    import math

    theta = math.radians(theta_deg)
    c = math.cos(theta)
    s = math.sin(theta)

    transformed: list[tuple[float, float]] = []
    for x, y in points:
        sx = x * scale
        sy = y * scale
        rx = sx * c - sy * s
        ry = sx * s + sy * c
        transformed.append((rx + tx, ry + ty))
    return transformed
