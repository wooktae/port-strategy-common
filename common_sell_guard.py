"""Common module for sell-side guards and risk flags.

Computes holding days, stop-loss, profit protection, MARKET BLOCK detailed conditions, and flow/score breakdown.
The final SELL/HOLD decision is handled by priority in a separate module, and this module performs no external integration.
"""

from __future__ import annotations

from port_strategy_common.common_context import CommonPositionContext
from port_strategy_common.common_result import CommonGuardDecision, CommonMarketDecision
from port_strategy_common.common_types import CommonMarketSignal
from port_strategy_common.common_utils import (
    common_get_config_bool,
    common_get_config_float,
    common_get_config_int,
    common_safe_float,
)


def common_is_min_holding_days(
    position: CommonPositionContext,
    config: dict | None = None,
) -> bool:
    """
    Whether the minimum holding-day protection applies.
    """
    min_holding_days_no_sell = common_get_config_int(
        config,
        "min_holding_days_no_sell",
        1,
    )

    return position.holding_days <= min_holding_days_no_sell


def common_is_hard_stop(
    position: CommonPositionContext,
    config: dict | None = None,
) -> bool:
    """
    Forced stop-loss condition.

    Criteria:
    - cum_return <= hard_stop_daily_return
    - or a raw today_return-family value is at or below the hard stop
    """
    hard_stop = common_get_config_float(
        config,
        "hard_stop_daily_return",
        -0.12,
    )

    if position.cum_return <= hard_stop:
        return True

    today_return = _common_get_position_today_return(position)
    if today_return <= hard_stop:
        return True

    return False


def common_is_existing_position_intraday_stop(
    position: CommonPositionContext,
    config: dict | None = None,
) -> bool:
    """
    Same-day sharp-drop stop-loss condition for an existing held position.
    """
    intraday_stop = common_get_config_float(
        config,
        "existing_position_intraday_stop_loss",
        -0.10,
    )

    today_return = _common_get_position_today_return(position)

    return today_return <= intraday_stop


def common_is_profit_protect(
    position: CommonPositionContext,
    config: dict | None = None,
) -> bool:
    """
    Protect profit when cumulative return is sufficient and the same-day drop is large.
    """
    profit_protect_cum_return = common_get_config_float(
        config,
        "profit_protect_cum_return",
        0.07,
    )
    profit_protect_daily_drop = common_get_config_float(
        config,
        "profit_protect_daily_drop",
        -0.04,
    )

    today_return = _common_get_position_today_return(position)

    return (
        position.cum_return >= profit_protect_cum_return
        and today_return <= profit_protect_daily_drop
    )


def common_is_early_risk_cut(
    position: CommonPositionContext,
    config: dict | None = None,
) -> bool:
    """
    Sharp-drop risk cut during the early holding-day window.
    """
    max_holding_days = common_get_config_int(
        config,
        "early_risk_cut_max_holding_days",
        2,
    )
    daily_return_threshold = common_get_config_float(
        config,
        "early_risk_cut_daily_return",
        -0.08,
    )

    today_return = _common_get_position_today_return(position)

    return (
        position.holding_days <= max_holding_days
        and today_return <= daily_return_threshold
    )


def common_is_early_cut(
    position: CommonPositionContext,
    config: dict | None = None,
) -> bool:
    """
    Cut when the cumulative loss is large during the early holding window.
    """
    early_cut_holding_days = common_get_config_int(
        config,
        "early_cut_holding_days",
        2,
    )
    early_cut_cum_return = common_get_config_float(
        config,
        "early_cut_cum_return",
        -0.07,
    )

    return (
        position.holding_days <= early_cut_holding_days
        and position.cum_return <= early_cut_cum_return
    )


def common_is_max_holding_days(
    position: CommonPositionContext,
    config: dict | None = None,
) -> bool:
    """
    Whether the maximum holding day has been reached.
    """
    max_holding_days = common_get_config_int(
        config,
        "max_holding_days",
        15,
    )

    return position.holding_days >= max_holding_days


def common_is_market_block(
    market: CommonMarketDecision,
) -> bool:
    return market.market_signal == CommonMarketSignal.BLOCK.value


def common_is_market_block_keep_allowed(
    position: CommonPositionContext,
    config: dict | None = None,
) -> bool:
    """
    Minimum condition under which a position can still be kept in the BLOCK regime.

    Skeleton of the required_keep_profit / strong survivor family of decisions from the existing strategy.
    """
    min_keep_profit = common_get_config_float(
        config,
        "market_block_min_keep_profit",
        0.021,
    )

    if position.cum_return >= min_keep_profit:
        return True

    stock = position.latest_stock
    if stock is None:
        return False

    strong_min_flow = common_get_config_float(
        config,
        "market_block_strong_min_flow",
        0.85,
    )
    strong_min_final = common_get_config_float(
        config,
        "market_block_strong_min_final",
        0.55,
    )
    strong_keep_profit = common_get_config_float(
        config,
        "market_block_strong_keep_profit",
        0.0,
    )

    return (
        stock.flow_pressure_score >= strong_min_flow
        and stock.final_score >= strong_min_final
        and position.cum_return >= strong_keep_profit
    )


def common_is_market_block_quality_drop(
    position: CommonPositionContext,
    config: dict | None = None,
) -> bool:
    """
    Quality-drop decision in the BLOCK regime.

    Cannot be decided when latest_stock is absent.
    """
    stock = position.latest_stock
    if stock is None:
        return False

    quality_drop_flow = common_get_config_float(
        config,
        "market_block_quality_drop_flow",
        0.20,
    )
    quality_drop_final = common_get_config_float(
        config,
        "market_block_quality_drop_final",
        0.15,
    )

    return (
        stock.flow_pressure_score <= quality_drop_flow
        or stock.final_score <= quality_drop_final
    )


def common_is_market_block_both_weak(
    position: CommonPositionContext,
    config: dict | None = None,
) -> bool:
    """
    Simultaneous flow/score weakness in the BLOCK regime.
    """
    stock = position.latest_stock
    if stock is None:
        return False

    min_holding_days = common_get_config_int(
        config,
        "market_block_both_weak_min_holding_days",
        4,
    )
    weak_flow = common_get_config_float(
        config,
        "market_block_both_weak_flow",
        0.40,
    )
    weak_final = common_get_config_float(
        config,
        "market_block_both_weak_final",
        0.28,
    )

    return (
        position.holding_days >= min_holding_days
        and stock.flow_pressure_score <= weak_flow
        and stock.final_score <= weak_final
    )


def common_is_market_block_flow_only_weak(
    position: CommonPositionContext,
    config: dict | None = None,
) -> bool:
    """
    Case where only the flow is weak in the BLOCK regime.
    """
    stock = position.latest_stock
    if stock is None:
        return False

    max_holding_days = common_get_config_int(
        config,
        "market_block_flow_only_weak_max_holding_days",
        3,
    )
    max_flow = common_get_config_float(
        config,
        "market_block_flow_only_weak_max_flow",
        0.45,
    )
    max_final = common_get_config_float(
        config,
        "market_block_flow_only_weak_max_final",
        0.40,
    )

    return (
        position.holding_days <= max_holding_days
        and stock.flow_pressure_score <= max_flow
        and stock.final_score >= max_final
    )


def common_is_market_block_mid_hold_neither_clear(
    position: CommonPositionContext,
    config: dict | None = None,
) -> bool:
    """
    BLOCK mid-term mixed/unclear type.
    """
    stock = position.latest_stock
    if stock is None:
        return False

    min_holding_days = common_get_config_int(
        config,
        "market_block_mid_hold_neither_clear_min_holding_days",
        4,
    )
    max_holding_days = common_get_config_int(
        config,
        "market_block_mid_hold_neither_clear_max_holding_days",
        5,
    )
    max_flow = common_get_config_float(
        config,
        "market_block_mid_hold_neither_clear_max_flow",
        0.95,
    )
    max_final = common_get_config_float(
        config,
        "market_block_mid_hold_neither_clear_max_final",
        0.60,
    )

    return (
        min_holding_days <= position.holding_days <= max_holding_days
        and stock.flow_pressure_score < max_flow
        and stock.final_score < max_final
    )


def common_is_stale_loser(
    position: CommonPositionContext,
    config: dict | None = None,
) -> bool:
    """
    Stale loser: held for a long time yet weak in loss/flow.
    """
    stock = position.latest_stock
    if stock is None:
        return False

    min_holding_days = common_get_config_int(
        config,
        "stale_loser_min_holding_days",
        4,
    )
    cum_return_threshold = common_get_config_float(
        config,
        "stale_loser_cum_return",
        -0.02,
    )
    flow_threshold = common_get_config_float(
        config,
        "stale_loser_flow",
        -0.05,
    )

    return (
        position.holding_days >= min_holding_days
        and position.cum_return <= cum_return_threshold
        and stock.flow_pressure_score <= flow_threshold
    )


def common_is_flow_breakdown(
    position: CommonPositionContext,
    config: dict | None = None,
) -> bool:
    """
    Flow breakdown condition.
    """
    stock = position.latest_stock
    if stock is None:
        return False

    min_holding_days = common_get_config_int(
        config,
        "flow_breakdown_min_holding_days",
        4,
    )
    max_cum_return = common_get_config_float(
        config,
        "flow_breakdown_max_cum_return",
        0.02,
    )
    sell_flow_breakdown = common_get_config_float(
        config,
        "sell_flow_breakdown",
        -0.10,
    )

    return (
        position.holding_days >= min_holding_days
        and position.cum_return <= max_cum_return
        and stock.flow_pressure_score <= sell_flow_breakdown
    )


def common_is_score_breakdown(
    position: CommonPositionContext,
    config: dict | None = None,
) -> bool:
    """
    Score breakdown condition.
    """
    stock = position.latest_stock
    if stock is None:
        return False

    min_holding_days = common_get_config_int(
        config,
        "score_breakdown_min_holding_days",
        4,
    )
    max_cum_return = common_get_config_float(
        config,
        "score_breakdown_max_cum_return",
        0.01,
    )
    sell_final_breakdown = common_get_config_float(
        config,
        "sell_final_breakdown",
        0.00,
    )

    return (
        position.holding_days >= min_holding_days
        and position.cum_return <= max_cum_return
        and stock.final_score <= sell_final_breakdown
    )


def common_decide_sell_guard(
    position: CommonPositionContext,
    market: CommonMarketDecision,
    config: dict | None = None,
) -> CommonGuardDecision:
    """
    Common evaluation of SELL-related guard/risk flags.

    Note:
    - This does not finalize the SELL/HOLD decision.
    - Records which sell flags are set in detail.
    - The final SELL/HOLD decision is made by priority in common_sell_decision.py.
    """
    min_holding_days = common_is_min_holding_days(position, config)
    hard_stop = common_is_hard_stop(position, config)
    intraday_stop = common_is_existing_position_intraday_stop(position, config)
    profit_protect = common_is_profit_protect(position, config)
    early_risk_cut = common_is_early_risk_cut(position, config)
    early_cut = common_is_early_cut(position, config)
    max_holding_days = common_is_max_holding_days(position, config)

    market_block = common_is_market_block(market)
    market_block_keep_allowed = (
        common_is_market_block_keep_allowed(position, config)
        if market_block
        else False
    )
    market_block_quality_drop = (
        common_is_market_block_quality_drop(position, config)
        if market_block
        else False
    )
    market_block_both_weak = (
        common_is_market_block_both_weak(position, config)
        if market_block
        else False
    )
    market_block_flow_only_weak = (
        common_is_market_block_flow_only_weak(position, config)
        if market_block
        else False
    )
    market_block_mid_hold_neither_clear = (
        common_is_market_block_mid_hold_neither_clear(position, config)
        if market_block
        else False
    )

    stale_loser = common_is_stale_loser(position, config)
    flow_breakdown = common_is_flow_breakdown(position, config)
    score_breakdown = common_is_score_breakdown(position, config)

    sell_flags = {
        "min_holding_days": min_holding_days,
        "hard_stop": hard_stop,
        "intraday_stop": intraday_stop,
        "profit_protect": profit_protect,
        "early_risk_cut": early_risk_cut,
        "early_cut": early_cut,
        "max_holding_days": max_holding_days,
        "market_block": market_block,
        "market_block_keep_allowed": market_block_keep_allowed,
        "market_block_quality_drop": market_block_quality_drop,
        "market_block_both_weak": market_block_both_weak,
        "market_block_flow_only_weak": market_block_flow_only_weak,
        "market_block_mid_hold_neither_clear": market_block_mid_hold_neither_clear,
        "stale_loser": stale_loser,
        "flow_breakdown": flow_breakdown,
        "score_breakdown": score_breakdown,
    }

    active_reasons = [
        key for key, value in sell_flags.items()
        if value and key not in ("market_block_keep_allowed",)
    ]

    has_sell_risk = any(
        sell_flags[key]
        for key in (
            "hard_stop",
            "intraday_stop",
            "profit_protect",
            "early_risk_cut",
            "early_cut",
            "max_holding_days",
            "market_block_quality_drop",
            "market_block_both_weak",
            "market_block_flow_only_weak",
            "market_block_mid_hold_neither_clear",
            "stale_loser",
            "flow_breakdown",
            "score_breakdown",
        )
    )

    return CommonGuardDecision(
        passed=not has_sell_risk,
        reason="SELL_GUARD_RISK_DETECTED" if has_sell_risk else "SELL_GUARD_PASSED",
        detail={
            "ticker_code": position.ticker_code,
            "ticker_name": position.ticker_name,
            "current_date": position.current_date,
            "entry_date": position.entry_date,
            "holding_days": position.holding_days,
            "entry_price": position.entry_price,
            "current_price": position.current_price,
            "quantity": position.quantity,
            "remaining_qty": position.remaining_qty,
            "cum_return": position.cum_return,
            "today_return": _common_get_position_today_return(position),
            "market_signal": market.market_signal,
            "sell_flags": sell_flags,
            "active_reasons": active_reasons,
        },
    )


def _common_get_position_today_return(position: CommonPositionContext) -> float:
    """
    Extract a same-day return-family value from position.raw or latest_stock.
    """
    candidates = [
        position.raw.get("today_return"),
        position.raw.get("raw_today_return"),
        position.raw.get("daily_return"),
        position.raw.get("change_rate"),
    ]

    if position.latest_stock is not None:
        candidates.append(position.latest_stock.change_rate)
        candidates.append(position.latest_stock.raw.get("today_return"))
        candidates.append(position.latest_stock.raw.get("raw_today_return"))
        candidates.append(position.latest_stock.raw.get("daily_return"))

    for value in candidates:
        if value is None:
            continue
        return common_safe_float(value, 0.0)

    if position.entry_price > 0 and position.current_price > 0:
        return (position.current_price / position.entry_price) - 1.0

    return 0.0
