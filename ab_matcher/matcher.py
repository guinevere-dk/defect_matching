from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
import pandas as pd

from .scoring import score_from_distance

try:
    from scipy.spatial import cKDTree  # type: ignore
except Exception:  # pragma: no cover - fallback path
    cKDTree = None


@dataclass
class MatchResult:
    a_index: int
    b_index: int
    distance_um: float
    score: float


def _iter_radius_matches_bruteforce(
    a_points: np.ndarray,
    b_points: np.ndarray,
    radius_um: float,
) -> Iterable[tuple[int, np.ndarray]]:
    radius_sq = radius_um * radius_um
    for i, a in enumerate(a_points):
        deltas = b_points - a
        dist_sq = np.sum(deltas * deltas, axis=1)
        idx = np.where(dist_sq <= radius_sq)[0]
        yield i, idx


def find_matches(a_df: pd.DataFrame, b_df: pd.DataFrame, radius_um: float = 50.0) -> pd.DataFrame:
    """Find candidate matches in a radius and compute score."""
    a_points = a_df[["x_ref_um", "y_ref_um"]].to_numpy(dtype=float)
    b_points = b_df[["x_ref_um", "y_ref_um"]].to_numpy(dtype=float)

    results: list[MatchResult] = []

    if cKDTree is not None:
        tree = cKDTree(b_points)
        neighbors_per_a = tree.query_ball_point(a_points, radius_um)
        iterator = enumerate(neighbors_per_a)
    else:
        iterator = _iter_radius_matches_bruteforce(a_points, b_points, radius_um)

    for a_idx, b_indices in iterator:
        for b_idx in b_indices:
            distance = float(np.linalg.norm(a_points[a_idx] - b_points[b_idx]))
            score = score_from_distance(distance, radius_um)
            results.append(
                MatchResult(
                    a_index=int(a_idx),
                    b_index=int(b_idx),
                    distance_um=distance,
                    score=score,
                )
            )

    if not results:
        return pd.DataFrame(columns=["a_index", "b_index", "distance_um", "score"])

    return pd.DataFrame([r.__dict__ for r in results])
