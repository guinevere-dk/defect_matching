from __future__ import annotations

import sqlite3


def ensure_matches_table(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS matches (
            a_id TEXT NOT NULL,
            b_id TEXT NOT NULL,
            distance REAL NOT NULL,
            score REAL NOT NULL
        )
        """
    )
    conn.commit()


def insert_matches(conn: sqlite3.Connection, matches: dict[str, list[dict]]) -> int:
    ensure_matches_table(conn)
    rows = []
    for a_id, candidates in matches.items():
        for c in candidates:
            rows.append((a_id, c["b_id"], float(c["distance"]), float(c["score"])))

    conn.executemany(
        "INSERT INTO matches (a_id, b_id, distance, score) VALUES (?, ?, ?, ?)",
        rows,
    )
    conn.commit()
    return len(rows)
