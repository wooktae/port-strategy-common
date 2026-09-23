"""Common module for the base buy candidate filter.

Determines whether a BUY candidate passes based on the stock score, flow, volatility, intraday range, and similar criteria.
It also provides a helper that converts a backtest row into a common stock context, and it performs no external integration.
"""

from __future__ import annotations

from decimal import Decimal
from typing import Any

from port_strategy_common.common_context import CommonStockContext
from port_strategy_common.common_result import CommonFilterDecision, CommonMarketDecision
from port_strategy_common.common_utils import common_get_config_float, common_safe_float


def common_decide_buy_filter(
    stock: CommonStockContext,
    market: CommonMarketDecision,
    config: dict | None = None,
) -> CommonFilterDecision:
    """
    Common function for the base BUY candidate filter.

    Same direction as the existing backtest_filter.py conditions:
    - Exclude on no_signal_flag
    - Exclude on the short / volatility / intraday upper limits
    - Exclude on the flow / final minimum criteria
    - tape/info pass as an exception when flow is at or above flow_strong
    """

    final_score = Decimal(str(stock.final_score))
    flow = Decimal(str(stock.flow_pressure_score))
    tape = Decimal(str(stock.tape_score))
    info = Decimal(str(common_safe_float(stock.raw.get("info_score"), 0.0)))
    short = Decimal(str(stock.short_pressure_score))
    vol = Decimal(str(stock.volatility_score))
    intraday_range = Decimal(str(common_safe_float(stock.intraday_range, 0.0)))

    no_signal = bool(stock.raw.get("no_signal_flag"))

    if no_signal:
        return CommonFilterDecision(
            passed=False,
            reason="FILTER_NO_SIGNAL",
            detail={
                "ticker_code": stock.ticker_code,
                "no_signal_flag": True,
            },
        )

    max_short_pressure = Decimal(str(common_get_config_float(config, "max_short_pressure", 0.80)))
    max_volatility_20d = Decimal(str(common_get_config_float(config, "max_volatility_20d", 0.08)))
    max_intraday_range = Decimal(str(common_get_config_float(config, "max_intraday_range", 0.15)))

    flow_min = Decimal(str(common_get_config_float(config, "flow_min", 0.62)))
    flow_strong = Decimal(str(common_get_config_float(config, "flow_strong", 0.03)))

    final_min = Decimal(str(common_get_config_float(config, "final_min", 0.070)))

    tape_min = Decimal(str(common_get_config_float(config, "tape_min", -0.15)))
    info_min = Decimal(str(common_get_config_float(config, "info_min", -0.10)))

    required_flow_min = max(flow_min, Decimal(str(market.min_flow)))
    required_final_min = max(final_min, Decimal(str(market.min_score)))

    if short > max_short_pressure:
        return CommonFilterDecision(
            passed=False,
            reason="FILTER_SHORT_PRESSURE_HIGH",
            detail={
                "ticker_code": stock.ticker_code,
                "short_pressure_score": float(short),
                "max_short_pressure": float(max_short_pressure),
            },
        )

    if vol > max_volatility_20d:
        return CommonFilterDecision(
            passed=False,
            reason="FILTER_VOLATILITY_HIGH",
            detail={
                "ticker_code": stock.ticker_code,
                "volatility_score": float(vol),
                "max_volatility_20d": float(max_volatility_20d),
            },
        )

    if intraday_range > max_intraday_range:
        return CommonFilterDecision(
            passed=False,
            reason="FILTER_INTRADAY_RANGE_HIGH",
            detail={
                "ticker_code": stock.ticker_code,
                "intraday_range": float(intraday_range),
                "max_intraday_range": float(max_intraday_range),
            },
        )

    if flow < required_flow_min:
        return CommonFilterDecision(
            passed=False,
            reason="FILTER_FLOW_SCORE_LOW",
            detail={
                "ticker_code": stock.ticker_code,
                "flow_pressure_score": float(flow),
                "required_flow_min": float(required_flow_min),
                "market_signal": market.market_signal,
            },
        )

    if final_score < required_final_min:
        return CommonFilterDecision(
            passed=False,
            reason="FILTER_FINAL_SCORE_LOW",
            detail={
                "ticker_code": stock.ticker_code,
                "final_score": float(final_score),
                "required_final_min": float(required_final_min),
                "market_signal": market.market_signal,
            },
        )

    if tape < tape_min and flow < flow_strong:
        return CommonFilterDecision(
            passed=False,
            reason="FILTER_TAPE_SCORE_LOW",
            detail={
                "ticker_code": stock.ticker_code,
                "tape_score": float(tape),
                "required_tape_min": float(tape_min),
                "flow_score": float(flow),
                "flow_strong": float(flow_strong),
            },
        )

    if info < info_min and flow < flow_strong:
        return CommonFilterDecision(
            passed=False,
            reason="FILTER_INFO_SCORE_LOW",
            detail={
                "ticker_code": stock.ticker_code,
                "info_score": float(info),
                "required_info_min": float(info_min),
                "flow_score": float(flow),
                "flow_strong": float(flow_strong),
            },
        )

    return CommonFilterDecision(
        passed=True,
        reason="FILTER_PASSED",
        detail={
            "ticker_code": stock.ticker_code,
            "final_score": float(final_score),
            "flow_pressure_score": float(flow),
            "tape_score": float(tape),
            "info_score": float(info),
            "short_pressure_score": float(short),
            "volatility_score": float(vol),
            "intraday_range": float(intraday_range),
            "market_signal": market.market_signal,
            "required_final_min": float(required_final_min),
            "required_flow_min": float(required_flow_min),
        },
    )


def common_filter_buy_candidates(
    stock_rows: list[dict[str, Any]],
    decision: CommonMarketDecision,
    config: dict | None = None,
) -> list[dict[str, Any]]:
    """
    List filter function identical to the existing backtest_filter.filter_buy_candidates().

    Role:
    1. Filter the row list
    2. Split into strong / normal
    3. Add extreme_score_flag / info_bonus_flag
    4. Sort by the existing sort_key
    5. Cut to decision.max_positions
    """

    strong: list[dict[str, Any]] = []
    normal: list[dict[str, Any]] = []

    for row in stock_rows:
        stock = common_build_stock_context_from_row(row)
        filter_decision = common_decide_buy_filter(
            stock=stock,
            market=decision,
            config=config,
        )

        if not filter_decision.passed:
            continue

        final_score = _d(row.get("final_score"))
        flow = _d(row.get("flow_score"))
        info = _d(row.get("info_score"))

        has_info = bool(row.get("has_info_flag"))

        final_extreme = _cfg_decimal(config, "final_extreme", "0.13")
        final_strong = _cfg_decimal(config, "final_strong", "0.08")
        flow_strong = _cfg_decimal(config, "flow_strong", "0.03")

        item = {
            **row,
            "extreme_score_flag": final_score >= final_extreme,
            "info_bonus_flag": has_info and info > Decimal("0"),
        }

        if final_score >= final_strong and flow >= flow_strong:
            strong.append(item)
        else:
            normal.append(item)

    strong.sort(key=common_buy_candidate_sort_key, reverse=True)
    normal.sort(key=common_buy_candidate_sort_key, reverse=True)

    merged = strong + normal

    if decision.max_positions > 0:
        merged = merged[: decision.max_positions]

    return merged


def common_build_stock_context_from_row(row: dict[str, Any]) -> CommonStockContext:
    """
    Convert a backtest stock row -> CommonStockContext.

    Based on the existing backtest_filter.py field names:
    - flow_score -> flow_pressure_score
    - volatility_20d -> volatility_score
    - info_score / has_info_flag / no_signal_flag are kept in raw
    """

    return CommonStockContext(
        trade_date=str(row.get("date", "TEST")),
        ticker_code=str(row.get("ticker_code", row.get("code", ""))),
        ticker_name=row.get("ticker_name", row.get("stock_name")),
        final_score=common_safe_float(row.get("final_score"), 0.0),
        flow_pressure_score=common_safe_float(row.get("flow_score"), 0.0),
        tape_score=common_safe_float(row.get("tape_score"), 0.0),
        short_pressure_score=common_safe_float(row.get("short_pressure_score"), 0.0),
        volatility_score=common_safe_float(row.get("volatility_20d"), 0.0),
        close_price=common_safe_float(row.get("close_price"), 0.0)
        if row.get("close_price") is not None
        else None,
        change_rate=common_safe_float(row.get("change_rate"), 0.0)
        if row.get("change_rate") is not None
        else None,
        intraday_range=common_safe_float(row.get("intraday_range"), 0.0),
        trading_value=common_safe_float(row.get("trading_value"), 0.0)
        if row.get("trading_value") is not None
        else None,
        raw=dict(row),
    )


def common_buy_candidate_sort_key(row: dict[str, Any]):
    """
    Same as the existing backtest_filter.py sort_key.

    Used with reverse=True:
    - highest final_score first
    - highest flow_score first
    - highest tape_score first
    - highest info_score first
    - lowest short_pressure_score first
    """
    return (
        _d(row.get("final_score")),
        _d(row.get("flow_score")),
        _d(row.get("tape_score")),
        _d(row.get("info_score")),
        -_d(row.get("short_pressure_score")),
    )


def _d(value: Any, default: str = "0") -> Decimal:
    return Decimal(str(common_safe_float(value, float(default))))


def _cfg_decimal(config: dict | None, key: str, default: str) -> Decimal:
    if not config:
        return Decimal(default)

    value = config.get(key)
    if value is None:
        return Decimal(default)

    return Decimal(str(value))
