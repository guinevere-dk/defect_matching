from __future__ import annotations


def score_from_distance(distance_um: float, radius_um: float = 50.0) -> float:
    """Linear score where 0um => 100 and radius => 0."""
    if distance_um < 0:
        raise ValueError("distance_um must be >= 0")
    if radius_um <= 0:
        raise ValueError("radius_um must be > 0")

    score = 100.0 * (1.0 - (distance_um / radius_um))
    return max(0.0, min(100.0, score))
