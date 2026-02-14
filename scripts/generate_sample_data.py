from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


RNG = np.random.default_rng(7)


def main() -> None:
    out_dir = Path("data")
    out_dir.mkdir(parents=True, exist_ok=True)

    a_count = 10
    b_count = 40

    a_x = RNG.uniform(0, 1000, size=a_count)
    a_y = RNG.uniform(0, 1000, size=a_count)
    a_df = pd.DataFrame({"a_id": [f"A{i:03d}" for i in range(a_count)], "x_a_um": a_x, "y_a_um": a_y})

    # Build B in reference space close to transformed A for some rows.
    b_x = RNG.uniform(0, 1200, size=b_count)
    b_y = RNG.uniform(0, 1200, size=b_count)
    b_x[:5] = a_x[:5] + RNG.normal(0, 3, size=5)
    b_y[:5] = a_y[:5] + RNG.normal(0, 3, size=5)

    b_df = pd.DataFrame({"b_id": [f"B{i:03d}" for i in range(b_count)], "x_ref_um": b_x, "y_ref_um": b_y})

    config = {
        "scale_x": 1.0,
        "scale_y": 1.0,
        "rotation_deg": 0.0,
        "offset_x": 0.0,
        "offset_y": 0.0,
    }

    a_df.to_csv(out_dir / "a_sample.csv", index=False)
    b_df.to_csv(out_dir / "b_sample.csv", index=False)
    with (out_dir / "transform_config.sample.json").open("w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)

    print("Generated sample data under data/")


if __name__ == "__main__":
    main()
