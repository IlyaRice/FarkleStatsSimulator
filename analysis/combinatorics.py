"""Exact enumeration of every N-dice roll to compute EV and bust odds."""
from __future__ import annotations

import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

import itertools
import logging
from collections.abc import Mapping
from typing import Dict, Tuple

from simulator.scoring import total_points

_LOGGER = logging.getLogger(__name__)


def _generate_all_rolls(num_dice: int) -> Tuple[Tuple[int, ...], ...]:
    """Return a tuple containing every possible *ordered* roll outcome."""
    return tuple(itertools.product(range(1, 7), repeat=num_dice))


def expectation_and_bust(num_dice: int) -> Tuple[float, float]:
    """Compute E[score] and P(bust) for a single throw of *num_dice* dice.

    Uses brute-force enumeration (6ⁿ states), so avoid n > 5.

    Args:
        num_dice: Between 1 and 5 inclusive.

    Returns:
        (expected_value, bust_probability)
    """
    if not 1 <= num_dice <= 5:
        raise ValueError("num_dice must be 1 … 5")

    rolls = _generate_all_rolls(num_dice)
    total_states = len(rolls)

    score_sum = 0.0
    bust_count = 0

    for outcome in rolls:
        pts = total_points(outcome)
        score_sum += pts
        if pts == 0:
            bust_count += 1

    ev = score_sum / total_states
    p_bust = bust_count / total_states
    _LOGGER.info(
        "N=%d dice → EV=%0.3f  P(bust)=%0.3f",
        num_dice,
        ev,
        p_bust,
    )
    return ev, p_bust


def table_1_to_5() -> Dict[int, Tuple[float, float]]:
    """Convenience: compute EV & P(bust) for N = 1…5 dice."""
    return {n: expectation_and_bust(n) for n in range(1, 6)}


if __name__ == "__main__":  # Manual smoke test
    from pprint import pprint

    logging.basicConfig(level=logging.INFO, format="%(message)s")
    pprint(table_1_to_5())
