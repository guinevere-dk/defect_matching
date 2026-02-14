from __future__ import annotations

import argparse
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="A-B equipment defect matching MVP")
    parser.add_argument("--a-csv", required=True, help="Path to A input CSV")
    parser.add_argument("--b-csv", required=True, help="Path to B history CSV")
    parser.add_argument("--transform-config", required=True, help="Path to transform JSON")
    parser.add_argument("--db-path", default="out/matches.sqlite3", help="Path to SQLite DB output")
    parser.add_argument("--summary-csv", default="out/summary.csv", help="Path to summary CSV output")
    parser.add_argument("--radius-um", type=float, default=50.0, help="Match radius in micrometers")
    parser.add_argument(
        "--score-threshold",
        type=float,
        default=95.0,
        help="Persist only matches with score >= threshold",
    )
    return parser


def run(args: argparse.Namespace) -> None:
    from . import db, io, matcher, transform
    from .summary import build_a_summary

    a_df = io.read_a_csv(args.a_csv)
    b_df = io.read_b_csv(args.b_csv)
    config = io.read_transform_config(args.transform_config)

    a_ref = transform.transform_a_to_reference(a_df, config)
    all_matches = matcher.find_matches(a_ref, b_df, radius_um=args.radius_um)

    summary_df = build_a_summary(a_ref, all_matches)

    persisted_count = 0
    if not all_matches.empty:
        enriched = all_matches.copy()
        enriched["a_id"] = a_ref.loc[enriched["a_index"], "a_id"].to_numpy()
        enriched["b_id"] = b_df.loc[enriched["b_index"], "b_id"].to_numpy()

        filtered = enriched[enriched["score"] >= args.score_threshold].copy()
        output_db = Path(args.db_path)
        output_db.parent.mkdir(parents=True, exist_ok=True)

        conn = db.init_db(output_db)
        try:
            persisted_count = db.persist_matches(conn, filtered)
        finally:
            conn.close()

    summary_path = Path(args.summary_csv)
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_df.to_csv(summary_path, index=False)

    print(f"Total A rows: {len(a_ref)}")
    print(f"Total candidate matches (within radius): {len(all_matches)}")
    print(f"Persisted matches (score >= {args.score_threshold}): {persisted_count}")
    print(f"Summary written to: {summary_path}")


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()
