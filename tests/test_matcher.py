from matcher import match_points


def test_sample_matching_conditions() -> None:
    a_points = [
        ("A1", (0.0, 0.0)),
        ("A2", (10.0, 10.0)),
        ("A3", (100.0, 100.0)),
    ]
    b_points = [
        ("B1", (0.5, 0.0), 0.95),
        ("B2", (1.0, 0.0), 0.90),
        ("B3", (1.5, 0.0), 0.10),  # within radius but excluded by score
        ("B4", (9.5, 10.0), 0.99),
    ]

    matches, stats = match_points(
        a_points,
        b_points,
        radius=2.0,
        score_threshold=0.8,
        max_matches_per_a=2,
    )

    assert any(len(cands) == 2 for cands in matches.values())
    assert any(len(cands) == 0 for cands in matches.values())
    assert stats["excluded_due_to_score"] >= 1
