from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, Mapping


@dataclass(frozen=True)
class ScoringConfig:
    radius_um: float
    distance_penalty_at_radius: float
    type_match_bonus: float
    type_mismatch_penalty: float
    score_threshold: float


def _to_float(mapping: Mapping[str, Any], key: str) -> float:
    if key not in mapping:
        raise KeyError(f"Missing scoring config key: {key}")
    return float(mapping[key])


def load_scoring_config(path: str) -> ScoringConfig:
    """Load scoring config from a JSON or YAML file."""
    config_path = Path(path)
    suffix = config_path.suffix.lower()

    with config_path.open("r", encoding="utf-8") as f:
        if suffix == ".json":
            data = json.load(f)
        elif suffix in {".yaml", ".yml"}:
            try:
                import yaml  # type: ignore
            except ImportError as exc:
                raise ImportError(
                    "PyYAML is required to load YAML scoring config files"
                ) from exc
            data = yaml.safe_load(f)
        else:
            # Fallback: try JSON first, then YAML if available.
            raw = f.read()
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                try:
                    import yaml  # type: ignore
                except ImportError as exc:
                    raise ValueError(
                        f"Unsupported config format for {path}; use .json or .yaml/.yml"
                    ) from exc
                data = yaml.safe_load(raw)

    if not isinstance(data, Mapping):
        raise ValueError("Scoring config must be a mapping/object")

    return ScoringConfig(
        radius_um=_to_float(data, "radius_um"),
        distance_penalty_at_radius=_to_float(data, "distance_penalty_at_radius"),
        type_match_bonus=_to_float(data, "type_match_bonus"),
        type_mismatch_penalty=_to_float(data, "type_mismatch_penalty"),
        score_threshold=_to_float(data, "score_threshold"),
    )


def compute_score(distance_um: float, a_type: str, b_type: str, cfg: ScoringConfig) -> float:
    distance_score = 100.0 - (float(distance_um) / cfg.radius_um) * cfg.distance_penalty_at_radius
    if a_type == b_type:
        score = distance_score + cfg.type_match_bonus
    else:
        score = distance_score - cfg.type_mismatch_penalty
    return max(0.0, min(100.0, score))
