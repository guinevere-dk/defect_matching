import pytest

from transform import transform_points


def test_known_point_transforms_with_config() -> None:
    points = [(1.0, 0.0), (0.0, 1.0)]
    config = {"scale": 2.0, "rotation_deg": 90.0, "translation": (1.0, -1.0)}

    result = transform_points(points, config)

    assert result[0] == pytest.approx((1.0, 1.0))
    assert result[1] == pytest.approx((-1.0, -1.0))
