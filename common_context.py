"""Collection of context dataclasses fed into shared strategy decisions.

Conveys market, stock, and held-position state in the same shape across the backtest and daily flows.
Holds only values prepared by the caller, without DB access, external API calls, or file IO.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class CommonMarketContext:
    trade_date: str

    market_regime_score: float = 0.0
    breadth_pressure_score: float = 0.0
    flow_pressure_score: float = 0.0
    macro_pressure_score: float = 0.0
    program_pressure_score: float = 0.0

    vix_return: float | None = None
    global_risk_score: float | None = None

    raw: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class CommonStockContext:
    trade_date: str
    ticker_code: str
    ticker_name: str | None = None

    final_score: float = 0.0
    flow_pressure_score: float = 0.0
    tape_score: float = 0.0
    short_pressure_score: float = 0.0
    volatility_score: float = 0.0

    close_price: float | None = None
    change_rate: float | None = None
    intraday_range: float | None = None
    trading_value: float | None = None

    raw: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class CommonPositionContext:
    ticker_code: str
    current_date: str

    entry_date: str | None = None
    ticker_name: str | None = None

    holding_days: int = 0
    entry_price: float = 0.0
    current_price: float = 0.0
    quantity: int = 0
    remaining_qty: int = 0
    cum_return: float = 0.0

    latest_stock: CommonStockContext | None = None
    latest_market: CommonMarketContext | None = None

    raw: dict[str, Any] = field(default_factory=dict)
