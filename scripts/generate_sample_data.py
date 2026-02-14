from __future__ import annotations

import csv
import json
from pathlib import Path


def _write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as fp:
        writer = csv.DictWriter(fp, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    data_dir = Path("data")
    data_dir.mkdir(parents=True, exist_ok=True)

    a_rows = [
        {"a_id": 1, "text": "Alpha Defect"},
        {"a_id": 2, "text": "Beta Defect"},
        {"a_id": 3, "text": "Gamma Defect"},
        {"a_id": 4, "text": "No Match Defect"},
    ]
    b_rows = [
        {"b_id": 10, "text": "alpha defect"},
        {"b_id": 11, "text": "beta defect"},
        {"b_id": 12, "text": "gamma defect"},
        {"b_id": 13, "text": "gamma defect"},
        {"b_id": 14, "text": "unrelated"},
    ]

    transform_config = {"text_column": "text", "lowercase": True, "strip": True}
    scoring_config = {"b_text_column": "text", "lowercase": True, "strip": True}

    _write_csv(data_dir / "sample_a.csv", a_rows, ["a_id", "text"])
    _write_csv(data_dir / "sample_b.csv", b_rows, ["b_id", "text"])

    (data_dir / "transform_config.json").write_text(json.dumps(transform_config, indent=2), encoding="utf-8")
    (data_dir / "scoring_config.json").write_text(json.dumps(scoring_config, indent=2), encoding="utf-8")

    print("Generated sample data and configs in ./data")


if __name__ == "__main__":
    main()
