from __future__ import annotations

from typing import Iterable, List

import numpy as np
import pandas as pd

from .scoring import ScoringConfig, compute_score

REQUIRED_A_COLUMNS = {"a_id", "x_ref_um", "y_ref_um", "defect_type"}
REQUIRED_B_COLUMNS = {"b_id", "x_ref_um", "y_ref_um", "defect_type"}
OUTPUT_COLUMNS = [
    "a_id",
    "b_id",
    "distance_um",
    "score",
    "a_x_ref_um",
    "a_y_ref_um",
    "b_x_ref_um",
    "b_y_ref_um",
    "a_defect_type",
    "b_defect_type",
]


def _validate_columns(df: pd.DataFrame, required: set[str], name: str) -> None:
    missing = required.difference(df.columns)
    if missing:
        missing_str = ", ".join(sorted(missing))
        raise ValueError(f"{name} missing required columns: {missing_str}")


def _candidate_lists_with_kdtree(
    a_points: np.ndarray, b_points: np.ndarray, radius_um: float
) -> Iterable[List[int]]:
    from scipy.spatial import cKDTree  # type: ignore

    tree = cKDTree(b_points)
    return tree.query_ball_point(a_points, r=radius_um)


def _candidate_lists_bruteforce(
    a_points: np.ndarray, b_points: np.ndarray, radius_um: float
) -> Iterable[List[int]]:
    radius_sq = radius_um * radius_um
    for a_pt in a_points:
        dx = b_points[:, 0] - a_pt[0]
        dy = b_points[:, 1] - a_pt[1]
        dist_sq = dx * dx + dy * dy
        idx = np.where(dist_sq <= radius_sq)[0].tolist()
        yield idx


def match_a_to_b(
    a_ref_df: pd.DataFrame,
    b_df: pd.DataFrame,
    cfg: ScoringConfig,
) -> pd.DataFrame:
    _validate_columns(a_ref_df, REQUIRED_A_COLUMNS, "a_ref_df")
    _validate_columns(b_df, REQUIRED_B_COLUMNS, "b_df")

    if a_ref_df.empty or b_df.empty:
        return pd.DataFrame(columns=OUTPUT_COLUMNS)

    a = a_ref_df[["a_id", "x_ref_um", "y_ref_um", "defect_type"]].copy()
    b = b_df[["b_id", "x_ref_um", "y_ref_um", "defect_type"]].copy()

    a_points = a[["x_ref_um", "y_ref_um"]].to_numpy(dtype=float)
    b_points = b[["x_ref_um", "y_ref_um"]].to_numpy(dtype=float)

    try:
        candidate_lists = _candidate_lists_with_kdtree(a_points, b_points, cfg.radius_um)
    except Exception:
        candidate_lists = _candidate_lists_bruteforce(a_points, b_points, cfg.radius_um)

    rows = []
    for a_idx, b_candidates in enumerate(candidate_lists):
        if not b_candidates:
            continue

        a_row = a.iloc[a_idx]
        ax = float(a_row["x_ref_um"])
        ay = float(a_row["y_ref_um"])
        a_type = str(a_row["defect_type"])

        for b_idx in b_candidates:
            b_row = b.iloc[b_idx]
            bx = float(b_row["x_ref_um"])
            by = float(b_row["y_ref_um"])
            distance_um = float(np.hypot(ax - bx, ay - by))
            score = compute_score(distance_um, a_type, str(b_row["defect_type"]), cfg)
            if score < cfg.score_threshold:
                continue

            rows.append(
                {
                    "a_id": a_row["a_id"],
                    "b_id": b_row["b_id"],
                    "distance_um": distance_um,
                    "score": score,
                    "a_x_ref_um": ax,
                    "a_y_ref_um": ay,
                    "b_x_ref_um": bx,
                    "b_y_ref_um": by,
                    "a_defect_type": a_type,
                    "b_defect_type": str(b_row["defect_type"]),
                }
            )

    if not rows:
        return pd.DataFrame(columns=OUTPUT_COLUMNS)

    out_df = pd.DataFrame(rows, columns=OUTPUT_COLUMNS)
    out_df = out_df.sort_values(
        by=["a_id", "score", "distance_um"],
        ascending=[True, False, True],
        kind="mergesort",
    ).reset_index(drop=True)
    return out_df
