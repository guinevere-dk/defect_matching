from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd


DDL = """
CREATE TABLE IF NOT EXISTS matches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    a_id TEXT NOT NULL,
    b_id TEXT NOT NULL,
    distance_um REAL NOT NULL,
    score REAL NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""


def init_db(db_path: str | Path) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.execute(DDL)
    conn.commit()
    return conn


def persist_matches(conn: sqlite3.Connection, matches_df: pd.DataFrame) -> int:
    if matches_df.empty:
        return 0

    rows = matches_df[["a_id", "b_id", "distance_um", "score"]].to_records(index=False)
    conn.executemany(
        "INSERT INTO matches (a_id, b_id, distance_um, score) VALUES (?, ?, ?, ?)",
        [tuple(row) for row in rows],
    )
    conn.commit()
    return len(rows)
