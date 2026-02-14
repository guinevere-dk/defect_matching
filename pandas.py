from __future__ import annotations

import csv
from pathlib import Path
from typing import Any, Iterable


class DataFrame:
    def __init__(self, data: Iterable[dict[str, Any]] | None = None):
        self._rows = [dict(row) for row in (data or [])]
        col_order: list[str] = []
        for row in self._rows:
            for key in row.keys():
                if key not in col_order:
                    col_order.append(key)
        self._columns = col_order

    @property
    def columns(self) -> list[str]:
        return list(self._columns)

    @property
    def empty(self) -> bool:
        return len(self._rows) == 0

    def to_records(self) -> list[dict[str, Any]]:
        return [dict(row) for row in self._rows]

    def to_csv(self, path: str | Path, index: bool = False) -> None:
        _ = index
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open("w", newline="", encoding="utf-8") as fp:
            writer = csv.DictWriter(fp, fieldnames=self._columns)
            writer.writeheader()
            for row in self._rows:
                writer.writerow({col: row.get(col, "") for col in self._columns})

    def to_string(self, index: bool = False) -> str:
        _ = index
        if not self._rows:
            return "<empty>"
        widths = {col: len(col) for col in self._columns}
        for row in self._rows:
            for col in self._columns:
                widths[col] = max(widths[col], len(str(row.get(col, ""))))

        header = " ".join(col.ljust(widths[col]) for col in self._columns)
        lines = [header]
        for row in self._rows:
            lines.append(" ".join(str(row.get(col, "")).ljust(widths[col]) for col in self._columns))
        return "\n".join(lines)


def read_csv(path: str | Path) -> DataFrame:
    with Path(path).open("r", newline="", encoding="utf-8") as fp:
        reader = csv.DictReader(fp)
        rows: list[dict[str, Any]] = []
        for row in reader:
            parsed = {}
            for key, value in row.items():
                if value is None:
                    parsed[key] = value
                    continue
                if value.isdigit():
                    parsed[key] = int(value)
                else:
                    parsed[key] = value
            rows.append(parsed)
    return DataFrame(rows)
