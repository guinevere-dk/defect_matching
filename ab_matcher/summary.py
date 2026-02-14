from __future__ import annotations

import pandas as pd


def make_summary(a_df: pd.DataFrame, matches_df: pd.DataFrame) -> pd.DataFrame:
    """Build summary by A record with match counts and boolean matched flag."""
    if "a_id" not in a_df.columns:
        raise ValueError("a_df must contain 'a_id' column")

    counts: dict[int, int] = {}
    if "a_id" in matches_df.columns:
        for row in matches_df.to_records():
            a_id = row["a_id"]
            counts[a_id] = counts.get(a_id, 0) + 1

    seen: set[int] = set()
    out_rows = []
    for row in a_df.to_records():
        a_id = row["a_id"]
        if a_id in seen:
            continue
        seen.add(a_id)
        match_count = counts.get(a_id, 0)
        out_rows.append({"a_id": a_id, "matched": match_count > 0, "match_count": match_count})

    return pd.DataFrame(out_rows)
