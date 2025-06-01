"""Canonical truth-check: EV for five dice."""
from __future__ import annotations

from analysis.combinatorics import expectation_and_bust


def test_ev_five_dice() -> None:
    """Exact expectation should match hard-coded reference value."""
    ev_5, _ = expectation_and_bust(5)
    # Reference value from enumeration (run once, freeze here).
    assert abs(ev_5 - 28.289) < 1e-3