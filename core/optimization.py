"""Deterministic cash-flow, scenario and Pareto helpers shared by decision products."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ScenarioBand:
    """A bounded downside/base/upside result with an explicit loss probability."""

    downside: float
    base: float
    upside: float
    probability_of_loss: float

    def __post_init__(self) -> None:
        if not self.downside <= self.base <= self.upside:
            raise ValueError("scenario values must be ordered downside <= base <= upside")
        if not 0.0 <= self.probability_of_loss <= 1.0:
            raise ValueError("probability_of_loss must be between zero and one")


def bounded(value: float, lower: float = 0.0, upper: float = 100.0) -> float:
    return max(lower, min(upper, value))


def present_value(cashflows: Sequence[float], annual_discount_rate: float) -> float:
    """Return present value where element zero is the initial cash flow."""
    if annual_discount_rate <= -1:
        raise ValueError("discount rate must be greater than -100%")
    return sum(value / (1 + annual_discount_rate) ** year for year, value in enumerate(cashflows))


def internal_rate_of_return(cashflows: Sequence[float]) -> float | None:
    """Find a deterministic annual IRR by bisection, or return None when no root is bracketed."""
    if (
        len(cashflows) < 2
        or not any(value < 0 for value in cashflows)
        or not any(value > 0 for value in cashflows)
    ):
        return None
    low, high = -0.99, 10.0
    low_value = present_value(cashflows, low)
    high_value = present_value(cashflows, high)
    if low_value * high_value > 0:
        return None
    for _ in range(120):
        midpoint = (low + high) / 2
        value = present_value(cashflows, midpoint)
        if abs(value) < 1e-7:
            return midpoint
        if low_value * value <= 0:
            high = midpoint
        else:
            low, low_value = midpoint, value
    return (low + high) / 2


def pareto_front(
    candidates: Sequence[Mapping[str, float]], objective_names: Sequence[str]
) -> tuple[int, ...]:
    """Return indices not dominated when every named objective is maximised."""
    survivors: list[int] = []
    for index, candidate in enumerate(candidates):
        dominated = False
        for other_index, other in enumerate(candidates):
            if index == other_index:
                continue
            no_worse = all(other[name] >= candidate[name] for name in objective_names)
            strictly_better = any(other[name] > candidate[name] for name in objective_names)
            if no_worse and strictly_better:
                dominated = True
                break
        if not dominated:
            survivors.append(index)
    return tuple(survivors)


def ranking_stability(top_scores: Sequence[float]) -> str:
    """Describe how decisively the leading option separates from alternatives."""
    if not top_scores:
        return "Insufficient"
    if len(top_scores) == 1:
        return "Medium"
    gap = top_scores[0] - top_scores[1]
    return "High" if gap >= 8 else "Medium" if gap >= 3 else "Low"
