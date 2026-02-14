from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd


def save_matches_sqlite(matches_df: pd.DataFrame, db_path: str, table_name: str = "matches") -> None:
    db_file = Path(db_path)
    db_file.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_file) as conn:
        cur = conn.cursor()
        cur.execute(f"DROP TABLE IF EXISTS {table_name}")
        cur.execute(
            f"CREATE TABLE {table_name} (a_id INTEGER NOT NULL, b_id INTEGER NOT NULL, reference_text TEXT NOT NULL)"
        )
        rows = [
            (row["a_id"], row["b_id"], row["reference_text"])
            for row in matches_df.to_records()
        ]
        if rows:
            cur.executemany(f"INSERT INTO {table_name} (a_id, b_id, reference_text) VALUES (?, ?, ?)", rows)
        conn.commit()
