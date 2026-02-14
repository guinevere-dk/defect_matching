from __future__ import annotations

import pandas as pd


def build_a_summary(a_df: pd.DataFrame, all_matches_df: pd.DataFrame) -> pd.DataFrame:
    """Build per-A-row summary with matched 여부 + match_count."""
    summary = a_df[["a_id"]].copy()
    summary["match_count"] = 0

    if not all_matches_df.empty:
        counts = all_matches_df.groupby("a_index").size().rename("match_count")
        summary.loc[counts.index, "match_count"] = counts.to_numpy()

    summary["matched_여부"] = summary["match_count"] > 0
    return summary
