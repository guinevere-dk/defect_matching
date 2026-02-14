from __future__ import annotations

import pandas as pd


def _normalize(value: object, lowercase: bool, strip: bool) -> str:
    text = str(value)
    if lowercase:
        text = text.lower()
    if strip:
        text = text.strip()
    return text


def match_records(reference_df: pd.DataFrame, b_df: pd.DataFrame, config: dict) -> pd.DataFrame:
    b_text_col = config.get("b_text_column", "text")
    lowercase = bool(config.get("lowercase", True))
    strip = bool(config.get("strip", True))

    if b_text_col not in b_df.columns:
        raise ValueError(f"B DataFrame missing configured text column: {b_text_col}")

    b_index: dict[str, list[int]] = {}
    for row in b_df.to_records():
        key = _normalize(row.get(b_text_col, ""), lowercase=lowercase, strip=strip)
        b_index.setdefault(key, []).append(row["b_id"])

    matches = []
    for row in reference_df.to_records():
        key = _normalize(row.get("reference_text", ""), lowercase=lowercase, strip=strip)
        for b_id in b_index.get(key, []):
            matches.append({"a_id": row["a_id"], "b_id": b_id, "reference_text": row["reference_text"]})

    return pd.DataFrame(matches)
