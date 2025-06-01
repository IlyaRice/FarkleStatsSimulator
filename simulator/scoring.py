"""Detection and valuation of all scoring combinations for a single roll."""
from __future__ import annotations

import logging
from collections import Counter
from dataclasses import dataclass
from typing import List, Tuple

_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class Combination:
    """Represents one non-overlapping scoring combination."""

    dice: Tuple[int, ...]
    points: int
    name: str


# Lookup for multiples and singles (value, count) → points.
_POINTS_TABLE: dict[tuple[int, int], int] = {
    # Ones
    (1, 1): 10,
    (1, 2): 20,
    (1, 3): 100,
    (1, 4): 200,
    (1, 5): 1000,
    # Fives
    (5, 1): 5,
    (5, 2): 10,
    (5, 3): 50,
    (5, 4): 100,
    (5, 5): 500,
    # Triples+ of 2, 3, 4, 6
    (2, 3): 20,
    (2, 4): 40,
    (2, 5): 200,
    (3, 3): 30,
    (3, 4): 60,
    (3, 5): 300,
    (4, 3): 40,
    (4, 4): 80,
    (4, 5): 400,
    (6, 3): 60,
    (6, 4): 120,
    (6, 5): 600,
}

# Straights: need *exact* five dice.
_STRAIGHTS: dict[Tuple[int, ...], int] = {
    (1, 2, 3, 4, 5): 125,
    (2, 3, 4, 5, 6): 250,
}


def score_roll(roll: Tuple[int, ...]) -> List[Combination]:
    """Return all non-overlapping scoring combos found in *roll*.

    The function maximises total points greedily:
    - Straights override everything if present.
    - For each face value, it picks the single highest-valued grouping
      (e.g. four 1 s worth 200, not 3×1 + 1×1 = 110).

    Args:
        roll: Tuple of dice values exactly as rolled (length 1-5).

    Returns:
        List of :class:`Combination` objects in *arbitrary* order.
        Empty list ⇒ bust (0 points).
    """
    sorted_roll = tuple(sorted(roll))

    # Straight?
    if sorted_roll in _STRAIGHTS:
        points = _STRAIGHTS[sorted_roll]
        _LOGGER.debug("Straight detected %s → %s pts", sorted_roll, points)
        return [Combination(dice=sorted_roll, points=points, name="straight")]

    counts = Counter(sorted_roll)
    combos: list[Combination] = []

    for face, qty in counts.items():
        # Look up max-value grouping for this face.
        best_points = 0
        best_count = 0
        for k in range(qty, 0, -1):
            pts = _POINTS_TABLE.get((face, k), 0)
            if pts > best_points:
                best_points = pts
                best_count = k
        if best_points:
            used_dice = tuple([face] * best_count)
            combos.append(
                Combination(
                    dice=used_dice,
                    points=best_points,
                    name=f"{best_count}×{face}",
                )
            )

    return combos


def total_points(roll: Tuple[int, ...]) -> int:
    """Convenience wrapper: sum of all combination points in *roll*."""
    return sum(c.points for c in score_roll(roll))
