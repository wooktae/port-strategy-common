from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class CommonMarketDecision:
    market_signal: str
    base_exposure: float
    max_positions: int
    min_score: float
    min_flow: float
    reason: str
    detail: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class CommonFilterDecision:
    passed: bool
    reason: str
    detail: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class CommonGuardDecision:
    passed: bool
    reason: str
    detail: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class CommonSizingDecision:
    target_weight: float
    target_amount: float
    target_qty: int
    reason: str
    detail: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class CommonBuyDecision:
    signal: str
    passed: bool
    score: float
    target_weight: float
    target_amount: float
    target_qty: int
    reason: str
    detail: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class CommonSellDecision:
    signal: str
    should_sell: bool
    reason: str
    detail: dict[str, Any] = field(default_factory=dict)