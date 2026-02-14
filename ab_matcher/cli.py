from __future__ import annotations

import argparse

from ab_matcher.config import load_json_config
from ab_matcher.io import load_a_csv, load_b_csv, save_summary_csv
from ab_matcher.matching import match_records
from ab_matcher.storage import save_matches_sqlite
from ab_matcher.summary import make_summary
from ab_matcher.transform import transform_a_to_reference


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run A/B record matching pipeline")
    parser.add_argument("--a", required=True, help="Path to A CSV")
    parser.add_argument("--b", required=True, help="Path to B CSV")
    parser.add_argument("--transform", required=True, help="Path to transform config JSON")
    parser.add_argument("--scoring", required=True, help="Path to scoring config JSON")
    parser.add_argument("--db", required=True, help="Path to output sqlite DB")
    parser.add_argument("--out-summary", required=True, help="Path to output summary CSV")
    return parser


def main() -> None:
    args = build_parser().parse_args()

    a_df = load_a_csv(args.a)
    b_df = load_b_csv(args.b)

    transform_config = load_json_config(args.transform)
    scoring_config = load_json_config(args.scoring)

    reference_df = transform_a_to_reference(a_df, transform_config)
    matches_df = match_records(reference_df, b_df, scoring_config)

    save_matches_sqlite(matches_df, args.db)

    summary_df = make_summary(a_df, matches_df)
    save_summary_csv(summary_df, args.out_summary)

    print("Summary:")
    print(summary_df.to_string(index=False))


if __name__ == "__main__":
    main()
