import sqlite3

from db import insert_matches


def test_insert_matches_count_and_table_exists() -> None:
    conn = sqlite3.connect(":memory:")
    matches = {
        "A1": [
            {"b_id": "B1", "distance": 0.5, "score": 0.9},
            {"b_id": "B2", "distance": 1.0, "score": 0.8},
        ],
        "A2": [],
    }

    inserted = insert_matches(conn, matches)

    assert inserted == 2

    table_exists = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='matches'"
    ).fetchone()
    assert table_exists is not None

    row_count = conn.execute("SELECT COUNT(*) FROM matches").fetchone()[0]
    assert row_count == 2
