from __future__ import annotations

from pathlib import Path

import pandas as pd


_A_REQUIRED_COLUMNS = {"a_id", "text"}
_B_REQUIRED_COLUMNS = {"b_id", "text"}
_SUMMARY_REQUIRED_COLUMNS = {"a_id", "matched", "match_count"}


def _validate_columns(df: pd.DataFrame, required: set[str], source_name: str) -> None:
    missing = required - set(df.columns)
    if missing:
        missing_cols = ", ".join(sorted(missing))
        raise ValueError(f"{source_name} missing required columns: {missing_cols}")


def load_a_csv(path: str) -> pd.DataFrame:
    """Load A CSV and validate expected schema."""
    df = pd.read_csv(path)
    _validate_columns(df, _A_REQUIRED_COLUMNS, "A CSV")
    return df


def load_b_csv(path: str) -> pd.DataFrame:
    """Load B CSV and validate expected schema."""
    df = pd.read_csv(path)
    _validate_columns(df, _B_REQUIRED_COLUMNS, "B CSV")
    return df


def save_summary_csv(df: pd.DataFrame, path: str) -> None:
    """Write summary dataframe to CSV."""
    _validate_columns(df, _SUMMARY_REQUIRED_COLUMNS, "Summary DataFrame")
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output, index=False)
