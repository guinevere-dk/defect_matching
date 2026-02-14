# A-B Equipment Defect Matching (MVP)

MVP pipeline for matching A-equipment defect points to B-equipment historical points.

## Features

- Read **A CSV** in A coordinate space.
- Transform A points to reference coordinates.
- Find B neighbors within configurable radius (default **50um**).
- Score candidates by distance.
- Persist only high-confidence matches (`score >= 95`) to SQLite.
- Output per-A-row summary (`matched_여부`, `match_count`).

## Project Structure

```text
ab_matcher/
  __init__.py
  io.py
  transform.py
  scoring.py
  matcher.py
  db.py
  summary.py
  cli.py
scripts/
  generate_sample_data.py
data/
out/
tests/
```

## Input Schemas

### A CSV schema

Required columns:

- `a_id` (string): unique row identifier
- `x_a_um` (float): x in A coordinate system (um)
- `y_a_um` (float): y in A coordinate system (um)

Example:

```csv
a_id,x_a_um,y_a_um
A001,123.4,567.8
A002,150.0,590.1
```

### B CSV schema

Required columns:

- `b_id` (string): historical point identifier
- `x_ref_um` (float): x in reference coordinate system (um)
- `y_ref_um` (float): y in reference coordinate system (um)

Example:

```csv
b_id,x_ref_um,y_ref_um
B900,125.0,568.2
B901,300.0,100.0
```

## Transform Config Schema (JSON)

`--transform-config` expects JSON with:

- `scale_x` (float)
- `scale_y` (float)
- `rotation_deg` (float)
- `offset_x` (float)
- `offset_y` (float)

Transform order:

1. Scale (`x_a_um`, `y_a_um`)
2. Rotate by `rotation_deg`
3. Translate by offsets

Example:

```json
{
  "scale_x": 1.0,
  "scale_y": 1.0,
  "rotation_deg": 0.0,
  "offset_x": 0.0,
  "offset_y": 0.0
}
```

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## CLI Usage

```bash
python -m ab_matcher.cli --help
```

Run matching:

```bash
python -m ab_matcher.cli \
  --a-csv data/a_sample.csv \
  --b-csv data/b_sample.csv \
  --transform-config data/transform_config.sample.json \
  --db-path out/matches.sqlite3 \
  --summary-csv out/summary.csv \
  --radius-um 50 \
  --score-threshold 95
```

Outputs:

- SQLite DB (`matches` table) at `--db-path`
- Summary CSV at `--summary-csv` with:
  - `a_id`
  - `match_count`
  - `matched_여부`

## Sample Data

Generate sample CSV/config:

```bash
python scripts/generate_sample_data.py
```
