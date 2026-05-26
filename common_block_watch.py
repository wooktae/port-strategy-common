from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Any, Optional


@dataclass(frozen=True)
class CommonBlockWatchDecision:
    is_watch: bool
    watch_reason: str
    watch_detail: dict[str, Any]


def _to_decimal(value: Any) -> Optional[Decimal]:
    if value is None:
        return None

    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError):
        return None


def _get_value(source: Any, *names: str) -> Any:
    if source is None:
        return None

    if isinstance(source, dict):
        for name in names:
            if name in source:
                return source.get(name)
        return None

    for name in names:
        if hasattr(source, name):
            return getattr(source, name)

    return None


def evaluate_block_watch_candidate(
    *,
    market_signal: str,
    stock_context: Any,
    min_flow_score: Decimal = Decimal("0.75"),
    min_final_score: Decimal = Decimal("0.45"),
    max_volatility_20d: Decimal = Decimal("0.10"),
    max_intraday_range: Decimal = Decimal("0.12"),
) -> CommonBlockWatchDecision:
    """
    BLOCK 구간에서 실제 매수는 하지 않지만, 강한 예외 후보를 관찰 대상으로 선별한다.

    중요:
    - 이 함수는 주문/매수 신호를 만들지 않는다.
    - strategy_daily_signal / strategy_execution_order 와 분리해서 사용한다.
    - Sharpe, MDD, 누적수익률 계산에는 포함하지 않는다.
    """

    normalized_market_signal = (market_signal or "").upper()

    flow_score = _to_decimal(
        _get_value(stock_context, "flow_score", "buy_flow_score", "supply_score")
    )
    final_score = _to_decimal(
        _get_value(stock_context, "final_score", "buy_final_score", "total_score")
    )
    info_score = _to_decimal(
        _get_value(stock_context, "info_score", "buy_info_score")
    )
    volatility_20d = _to_decimal(
        _get_value(stock_context, "volatility_20d", "vol_20d")
    )
    intraday_range = _to_decimal(
        _get_value(stock_context, "intraday_range", "day_range")
    )
    short_pressure_score = _to_decimal(
        _get_value(stock_context, "short_pressure_score", "short_pressure")
    )

    watch_detail = {
        "market_signal": normalized_market_signal,
        "criteria": {
            "min_flow_score": str(min_flow_score),
            "min_final_score": str(min_final_score),
            "max_volatility_20d": str(max_volatility_20d),
            "max_intraday_range": str(max_intraday_range),
        },
        "scores": {
            "flow_score": str(flow_score) if flow_score is not None else None,
            "final_score": str(final_score) if final_score is not None else None,
            "info_score": str(info_score) if info_score is not None else None,
            "volatility_20d": str(volatility_20d) if volatility_20d is not None else None,
            "intraday_range": str(intraday_range) if intraday_range is not None else None,
            "short_pressure_score": str(short_pressure_score) if short_pressure_score is not None else None,
        },
        "failed_reasons": [],
    }

    if normalized_market_signal != "BLOCK":
        watch_detail["failed_reasons"].append("MARKET_NOT_BLOCK")
        return CommonBlockWatchDecision(
            is_watch=False,
            watch_reason="MARKET_NOT_BLOCK",
            watch_detail=watch_detail,
        )

    required_values = {
        "flow_score": flow_score,
        "final_score": final_score,
        "volatility_20d": volatility_20d,
        "intraday_range": intraday_range,
    }

    missing = [key for key, value in required_values.items() if value is None]
    if missing:
        watch_detail["failed_reasons"].append("MISSING_REQUIRED_SCORE")
        watch_detail["missing_fields"] = missing
        return CommonBlockWatchDecision(
            is_watch=False,
            watch_reason="MISSING_REQUIRED_SCORE",
            watch_detail=watch_detail,
        )

    if flow_score < min_flow_score:
        watch_detail["failed_reasons"].append("FLOW_SCORE_TOO_LOW")

    if final_score < min_final_score:
        watch_detail["failed_reasons"].append("FINAL_SCORE_TOO_LOW")

    if volatility_20d > max_volatility_20d:
        watch_detail["failed_reasons"].append("VOLATILITY_TOO_HIGH")

    if intraday_range > max_intraday_range:
        watch_detail["failed_reasons"].append("INTRADAY_RANGE_TOO_WIDE")

    if watch_detail["failed_reasons"]:
        return CommonBlockWatchDecision(
            is_watch=False,
            watch_reason=";".join(watch_detail["failed_reasons"]),
            watch_detail=watch_detail,
        )

    return CommonBlockWatchDecision(
        is_watch=True,
        watch_reason="BLOCK_STRONG_EXCEPTION_WATCH",
        watch_detail=watch_detail,
    )