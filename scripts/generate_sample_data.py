#!/usr/bin/env python3
"""Generate deterministic sample data and configs for defect matching demos."""

from __future__ import annotations

import csv
import json
import random
from pathlib import Path

TRANSFORM_CONFIG = {
    "scale": 1.0,
    "rotation_deg": 0.0,
    "tx_um": 1000.0,
    "ty_um": -500.0,
}

SCORING_CONFIG = {
    "radius_um": 50.0,
    "distance_penalty_at_radius": 5.0,
    "type_match_bonus": 2.0,
    "type_mismatch_penalty": 5.0,
    "score_threshold": 95.0,
}


def apply_transform(x_um: float, y_um: float) -> tuple[float, float]:
    """Apply the simple transform from A space into B reference space."""
    return (
        x_um * TRANSFORM_CONFIG["scale"] + TRANSFORM_CONFIG["tx_um"],
        y_um * TRANSFORM_CONFIG["scale"] + TRANSFORM_CONFIG["ty_um"],
    )


def main() -> None:
    random.seed(20240530)

    repo_root = Path(__file__).resolve().parents[1]
    data_dir = repo_root / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    sample_a = [
        # Handcrafted: this A record has two clear matches in B.
        {
            "a_id": "A001",
            "x_um": 1200.0,
            "y_um": 800.0,
            "ts": "2024-01-01T10:00:00Z",
            "defect_type": "scratch",
        },
        # Handcrafted: this A record has a nearby B candidate within radius,
        # but defect type mismatch should keep score below threshold.
        {
            "a_id": "A002",
            "x_um": 5000.0,
            "y_um": 2200.0,
            "ts": "2024-01-01T10:02:00Z",
            "defect_type": "pit",
        },
        # Handcrafted: this A record intentionally has no nearby B records.
        {
            "a_id": "A003",
            "x_um": 50.0,
            "y_um": 50.0,
            "ts": "2024-01-01T10:04:00Z",
            "defect_type": "particle",
        },
    ]

    # Add deterministic random A records to make the sample look realistic.
    for i in range(4, 10):
        sample_a.append(
            {
                "a_id": f"A{i:03d}",
                "x_um": round(random.uniform(100.0, 8000.0), 3),
                "y_um": round(random.uniform(100.0, 8000.0), 3),
                "ts": f"2024-01-01T10:{i:02d}:00Z",
                "defect_type": random.choice(["scratch", "pit", "particle", "stain"]),
            }
        )

    ax1, ay1 = apply_transform(1200.0, 800.0)
    ax2, ay2 = apply_transform(5000.0, 2200.0)

    sample_b = [
        # Two high-quality matches for A001.
        {
            "b_id": "B001",
            "x_ref_um": round(ax1 + 8.0, 3),
            "y_ref_um": round(ay1 - 6.0, 3),
            "ts": "2024-01-01T10:00:30Z",
            "defect_type": "scratch",
        },
        {
            "b_id": "B002",
            "x_ref_um": round(ax1 - 12.0, 3),
            "y_ref_um": round(ay1 + 9.0, 3),
            "ts": "2024-01-01T10:00:45Z",
            "defect_type": "scratch",
        },
        # Nearby candidate for A002 (distance ~10.4 um) but mismatched type.
        {
            "b_id": "B003",
            "x_ref_um": round(ax2 + 10.0, 3),
            "y_ref_um": round(ay2 - 3.0, 3),
            "ts": "2024-01-01T10:02:30Z",
            "defect_type": "scratch",
        },
    ]

    # Add deterministic random B noise points.
    for i in range(4, 14):
        sample_b.append(
            {
                "b_id": f"B{i:03d}",
                "x_ref_um": round(random.uniform(900.0, 9000.0), 3),
                "y_ref_um": round(random.uniform(-600.0, 7800.0), 3),
                "ts": f"2024-01-01T11:{i:02d}:00Z",
                "defect_type": random.choice(["scratch", "pit", "particle", "stain"]),
            }
        )

    with (data_dir / "sample_a.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["a_id", "x_um", "y_um", "ts", "defect_type"])
        writer.writeheader()
        writer.writerows(sample_a)

    with (data_dir / "sample_b.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["b_id", "x_ref_um", "y_ref_um", "ts", "defect_type"],
        )
        writer.writeheader()
        writer.writerows(sample_b)

    (data_dir / "transform_config.json").write_text(
        json.dumps(TRANSFORM_CONFIG, indent=2) + "\n",
        encoding="utf-8",
    )
    (data_dir / "scoring_config.json").write_text(
        json.dumps(SCORING_CONFIG, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
