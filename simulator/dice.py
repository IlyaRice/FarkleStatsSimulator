"""Random dice utilities: roll an arbitrary number of six-sided dice."""
from __future__ import annotations

import logging
import random
from typing import Tuple

logging.basicConfig(
    format="%(levelname)s:%(name)s:%(message)s",
    level=logging.INFO,
)
_LOGGER = logging.getLogger(__name__)


def roll(num_dice: int = 5, rng: random.Random | None = None) -> Tuple[int, ...]:
    """Roll *num_dice* six-sided dice.

    Args:
        num_dice: How many dice to roll (1–5 for this game variant).
        rng: Optional instance of :class:`random.Random` for determinism.

    Returns:
        Tuple of integers in **natural order of roll** (1–6 each).

    Raises:
        ValueError: If *num_dice* is less than 1.
    """
    if num_dice < 1:
        raise ValueError("num_dice must be at least 1")

    generator = rng or random
    result: Tuple[int, ...] = tuple(generator.randint(1, 6) for _ in range(num_dice))

    _LOGGER.debug("Rolled %s → %s", num_dice, result)
    return result
