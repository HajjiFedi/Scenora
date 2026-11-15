"""Calculs géométriques du plan 2D (sans IA)."""

from __future__ import annotations

Point = tuple[float, float]


def side_of_axis(a: Point, b: Point, p: Point, tolerance: float = 1e-9) -> int:
    """Côté de l'axe AB où se trouve P : 1 (gauche), -1 (droite) ou 0 (sur l'axe)."""
    cross = (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])
    if abs(cross) <= tolerance:
        return 0
    return 1 if cross > 0 else -1
