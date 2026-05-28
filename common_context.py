"""공통 전략 판단에 입력되는 context dataclass 모음.

시장, 종목, 보유 포지션 상태를 backtest와 daily 흐름에서 같은 형태로 전달한다.
DB 접근, 외부 API 호출, 파일 IO 없이 caller가 준비한 값만 담는다.
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
