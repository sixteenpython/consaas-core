from __future__ import annotations

import pytest

from core.optimization import ScenarioBand, internal_rate_of_return, pareto_front, present_value


def test_cash_flow_math_is_deterministic() -> None:
    cashflows = (-100.0, 60.0, 60.0)
    assert present_value(cashflows, 0.1) == pytest.approx(4.1322, abs=0.001)
    assert internal_rate_of_return(cashflows) == pytest.approx(0.13066, abs=0.0001)


def test_pareto_front_removes_only_dominated_candidates() -> None:
    candidates = (
        {"return": 80.0, "resilience": 70.0},
        {"return": 70.0, "resilience": 60.0},
        {"return": 65.0, "resilience": 90.0},
    )
    assert pareto_front(candidates, ("return", "resilience")) == (0, 2)


def test_scenario_band_rejects_incoherent_ranges() -> None:
    with pytest.raises(ValueError, match="ordered"):
        ScenarioBand(10, 5, 20, 0.3)
