from __future__ import annotations

from app.services.spatial.geometry import side_of_axis


def test_side_of_axis() -> None:
    a, b = (0.0, 0.0), (10.0, 0.0)
    assert side_of_axis(a, b, (5.0, 3.0)) == 1
    assert side_of_axis(a, b, (5.0, -3.0)) == -1
    assert side_of_axis(a, b, (20.0, 0.0)) == 0
