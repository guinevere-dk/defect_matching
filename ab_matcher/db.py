"""SQLite persistence helpers for A/B defect matches."""

from __future__ import annotations

import sqlite3
from datetime import datetime, timezone

import pandas as pd


_REQUIRED_COLUMNS = (
    "a_id",
    "b_id",
    "distance_um",
    "score",
    "a_x_ref_um",
    "a_y_ref_um",
    "b_x_ref_um",
    "b_y_ref_um",
)


def create_db(db_path: str) -> None:
    """Create the SQLite database and required tables/indexes if missing."""
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS matches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                a_id TEXT NOT NULL,
                b_id TEXT NOT NULL,
                distance_um REAL NOT NULL,
                score REAL NOT NULL,
                a_x_ref_um REAL NOT NULL,
                a_y_ref_um REAL NOT NULL,
                b_x_ref_um REAL NOT NULL,
                b_y_ref_um REAL NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_matches_a_id ON matches (a_id)"
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_matches_b_id ON matches (b_id)"
        )
        conn.commit()


def insert_matches(db_path: str, matches_df: pd.DataFrame) -> int:
    """Insert all rows from ``matches_df`` and return the inserted row count."""
    create_db(db_path)

    missing_columns = [col for col in _REQUIRED_COLUMNS if col not in matches_df.columns]
    if missing_columns:
        raise ValueError(f"matches_df is missing required columns: {missing_columns}")

    if matches_df.empty:
        return 0

    created_at = datetime.now(timezone.utc).isoformat()
    rows = [
        (
            str(row["a_id"]),
            str(row["b_id"]),
            float(row["distance_um"]),
            float(row["score"]),
            float(row["a_x_ref_um"]),
            float(row["a_y_ref_um"]),
            float(row["b_x_ref_um"]),
            float(row["b_y_ref_um"]),
            created_at,
        )
        for _, row in matches_df.iterrows()
    ]

    with sqlite3.connect(db_path) as conn:
        cursor = conn.executemany(
            """
            INSERT INTO matches (
                a_id,
                b_id,
                distance_um,
                score,
                a_x_ref_um,
                a_y_ref_um,
                b_x_ref_um,
                b_y_ref_um,
                created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            rows,
        )
        conn.commit()
        return cursor.rowcount if cursor.rowcount != -1 else len(rows)
