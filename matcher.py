from __future__ import annotations

import math
from collections.abc import Iterable


def _distance(p1: tuple[float, float], p2: tuple[float, float]) -> float:
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])


def match_points(
    a_points: Iterable[tuple[str, tuple[float, float]]],
    b_points: Iterable[tuple[str, tuple[float, float], float]],
    *,
    radius: float,
    score_threshold: float,
    max_matches_per_a: int = 2,
) -> tuple[dict[str, list[dict]], dict[str, int]]:
    """Match A points to nearby B candidates that exceed score threshold."""
    stored: dict[str, list[dict]] = {}
    excluded_due_to_score = 0

    b_points = list(b_points)
    for a_id, a_pos in a_points:
        candidates = []
        for b_id, b_pos, score in b_points:
            dist = _distance(a_pos, b_pos)
            if dist <= radius:
                if score >= score_threshold:
                    candidates.append({"b_id": b_id, "distance": dist, "score": score})
                else:
                    excluded_due_to_score += 1

        candidates.sort(key=lambda row: (row["distance"], -row["score"]))
        stored[a_id] = candidates[:max_matches_per_a]

    stats = {"excluded_due_to_score": excluded_due_to_score}
    return stored, stats
