from __future__ import annotations

import pandas as pd


def transform_a_to_reference(a_df: pd.DataFrame, config: dict) -> pd.DataFrame:
    text_col = config.get("text_column", "text")
    lowercase = bool(config.get("lowercase", True))
    strip = bool(config.get("strip", True))

    if text_col not in a_df.columns:
        raise ValueError(f"A DataFrame missing configured text column: {text_col}")

    out_rows = []
    for row in a_df.to_records():
        text = str(row.get(text_col, ""))
        if lowercase:
            text = text.lower()
        if strip:
            text = text.strip()
        out_rows.append({"a_id": row["a_id"], "reference_text": text})
    return pd.DataFrame(out_rows)
