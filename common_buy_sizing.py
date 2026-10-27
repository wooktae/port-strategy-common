"""Common module for buy sizing and backtest allocation.

Computes Daily/Execution single-stock sizing and backtest candidate list allocation under the same configuration criteria.
It handles only amount and quantity calculation, and does not perform order submission, DB storage, or external API calls.
"""

from __future__ import annotations

import math
from decimal import Decimal
from typing import Any

from port_strategy_common.common_context import CommonStockContext
from port_strategy_common.common_result import (
    CommonGuardDecision,
    CommonMarketDecision,
    CommonSizingDecision,
)
from port_strategy_common.common_utils import (
    common_clamp,
    common_get_config_float,
    common_safe_float,
)


# =========================================================
# Daily / Execution single-stock sizing function
# =========================================================

def common_calculate_buy_sizing(
    stock: CommonStockContext,
    market: CommonMarketDecision,
    guard: CommonGuardDecision,
    config: dict | None = None,
    *,
    available_cash: float,
    current_position_count: int = 0,
) -> CommonSizingDecision:
    """
    Common BUY sizing calculation function.

    This function is the single-stock sizing skeleton for Daily / Execution.
    It is separate from the existing backtest allocate_positions(),
    and equivalence validation against the existing backtest is handled in common_allocate_positions().
    """

    price = common_safe_float(stock.close_price, 0.0)
    cash = common_safe_float(available_cash, 0.0)

    if price <= 0:
        return CommonSizingDecision(
            target_weight=0.0,
            target_amount=0.0,
            target_qty=0,
            reason="SIZING_INVALID_PRICE",
            detail={
                "ticker_code": stock.ticker_code,
                "close_price": stock.close_price,
                "available_cash": available_cash,
            },
        )

    if cash <= 0:
        return CommonSizingDecision(
            target_weight=0.0,
            target_amount=0.0,
            target_qty=0,
            reason="SIZING_NO_AVAILABLE_CASH",
            detail={
                "ticker_code": stock.ticker_code,
                "close_price": price,
                "available_cash": cash,
            },
        )

    if market.max_positions <= 0:
        return CommonSizingDecision(
            target_weight=0.0,
            target_amount=0.0,
            target_qty=0,
            reason="SIZING_MARKET_NO_POSITION_ALLOWED",
            detail={
                "ticker_code": stock.ticker_code,
                "market_signal": market.market_signal,
                "max_positions": market.max_positions,
            },
        )

    if current_position_count >= market.max_positions:
        return CommonSizingDecision(
            target_weight=0.0,
            target_amount=0.0,
            target_qty=0,
            reason="SIZING_MAX_POSITION_REACHED",
            detail={
                "ticker_code": stock.ticker_code,
                "market_signal": market.market_signal,
                "current_position_count": current_position_count,
                "max_positions": market.max_positions,
            },
        )

    base_slot_weight = market.base_exposure / max(market.max_positions, 1)

    score_component = _common_calculate_score_component(stock, config)
    volatility_penalty = _common_calculate_volatility_penalty(stock, config)
    guard_multiplier, guard_reasons = _common_calculate_guard_multiplier(guard, config)

    raw_weight = base_slot_weight * score_component
    adjusted_weight = raw_weight * volatility_penalty * guard_multiplier

    min_position_size = common_get_config_float(config, "min_position_size", 0.05)
    max_position_size = common_get_config_float(config, "max_position_size", 0.35)

    target_weight = common_clamp(
        adjusted_weight,
        min_position_size if adjusted_weight > 0 else 0.0,
        max_position_size,
    )

    target_amount = cash * target_weight
    target_qty = math.floor(target_amount / price)

    if target_qty <= 0:
        return CommonSizingDecision(
            target_weight=target_weight,
            target_amount=target_amount,
            target_qty=0,
            reason="SIZING_TARGET_QTY_ZERO",
            detail={
                "ticker_code": stock.ticker_code,
                "close_price": price,
                "available_cash": cash,
                "target_weight": target_weight,
                "target_amount": target_amount,
                "base_slot_weight": base_slot_weight,
                "score_component": score_component,
                "volatility_penalty": volatility_penalty,
                "guard_multiplier": guard_multiplier,
                "guard_reasons": guard_reasons,
            },
        )

    return CommonSizingDecision(
        target_weight=target_weight,
        target_amount=target_amount,
        target_qty=target_qty,
        reason="SIZING_PASSED",
        detail={
            "ticker_code": stock.ticker_code,
            "market_signal": market.market_signal,
            "close_price": price,
            "available_cash": cash,
            "current_position_count": current_position_count,
            "max_positions": market.max_positions,
            "base_exposure": market.base_exposure,
            "base_slot_weight": base_slot_weight,
            "score_component": score_component,
            "volatility_penalty": volatility_penalty,
            "guard_multiplier": guard_multiplier,
            "guard_reasons": guard_reasons,
            "raw_weight": raw_weight,
            "adjusted_weight": adjusted_weight,
            "target_weight": target_weight,
            "target_amount": target_amount,
            "target_qty": target_qty,
        },
    )


def _common_calculate_score_component(
    stock: CommonStockContext,
    config: dict | None,
) -> float:
    final_weight = common_get_config_float(config, "final_weight", 0.65)
    flow_weight = common_get_config_float(config, "flow_weight", 0.25)
    tape_weight = common_get_config_float(config, "tape_weight", 0.10)
    info_bonus_weight = common_get_config_float(config, "info_bonus_weight", 0.05)

    info_score = common_safe_float(
        stock.raw.get("info_score", stock.raw.get("information_score", 0.0)),
        0.0,
    )

    raw_score = (
        stock.final_score * final_weight
        + stock.flow_pressure_score * flow_weight
        + stock.tape_score * tape_weight
        + max(info_score, 0.0) * info_bonus_weight
    )

    return common_clamp(raw_score, 0.10, 1.50)


def _common_calculate_volatility_penalty(
    stock: CommonStockContext,
    config: dict | None,
) -> float:
    vol_penalty_multiplier = common_get_config_float(config, "vol_penalty_multiplier", 16.0)
    volatility = common_safe_float(stock.volatility_score, 0.0)

    penalty = 1.0 - (volatility * vol_penalty_multiplier)

    return common_clamp(penalty, 0.20, 1.00)


def _common_calculate_guard_multiplier(
    guard: CommonGuardDecision,
    config: dict | None,
) -> tuple[float, list[str]]:
    risk_flags = guard.detail.get("risk_flags", {}) if guard and guard.detail else {}

    multiplier = 1.0
    reasons: list[str] = []

    if risk_flags.get("hot_chase"):
        multiplier *= common_get_config_float(config, "hot_chase_haircut", 0.20)
        reasons.append("hot_chase_haircut")

    if risk_flags.get("high_flow_soft_risk"):
        multiplier *= common_get_config_float(config, "high_flow_soft_haircut", 0.80)
        reasons.append("high_flow_soft_haircut")

    if risk_flags.get("buy_day_stop_risk"):
        multiplier *= common_get_config_float(config, "buy_day_stop_risk_haircut", 0.50)
        reasons.append("buy_day_stop_risk_haircut")

    if risk_flags.get("mid_flow_tight_range_risk"):
        multiplier *= common_get_config_float(config, "mid_flow_tight_range_haircut", 0.70)
        reasons.append("mid_flow_tight_range_haircut")

    return common_clamp(multiplier, 0.0, 1.0), reasons


# =========================================================
# Function that is 1:1 identical to the existing backtest allocate_positions()
# =========================================================

def common_allocate_positions(
    buy_candidates: list[dict[str, Any]],
    market_decision: CommonMarketDecision,
    config: dict | None = None,
) -> list[dict[str, Any]]:
    """
    List allocation function identical to the existing backtest_sizing.allocate_positions().

    Role:
    1. Compute raw_rank_score per candidate
    2. Apply the volatility penalty to compute adj_score
    3. Sort by adj_score / final_score / flow_score
    4. Cut to max_positions
    5. Distribute base_exposure by the adj_score ratio
    6. Clamp to min/max position_size
    7. Scale down proportionally when the total position_size sum exceeds base_exposure
    """

    base = _d(market_decision.base_exposure)

    if base <= 0 or not buy_candidates:
        return []

    adjusted: list[dict[str, Any]] = []

    for row in buy_candidates:
        raw_rank_score, adj_score = common_calculate_rank_score(row, config)

        adjusted.append(
            {
                **row,
                "raw_rank_score": raw_rank_score,
                "adj_score": adj_score,
            }
        )

    adjusted.sort(
        key=common_allocation_sort_key,
        reverse=True,
    )

    if market_decision.max_positions > 0:
        adjusted = adjusted[: market_decision.max_positions]

    total = sum(_d(r["adj_score"]) for r in adjusted if _d(r["adj_score"]) > 0)

    if total <= 0:
        return []

    result: list[dict[str, Any]] = []

    for i, row in enumerate(adjusted, 1):
        weight = _d(row["adj_score"]) / total
        size = weight * base
        size = _clamp(
            size,
            _cfg_decimal(config, "min_position_size", "0.05"),
            _cfg_decimal(config, "max_position_size", "0.35"),
        )

        result.append(
            {
                **row,
                "rank_num": i,
                "weight": weight,
                "position_size": size,
            }
        )

    total_size = sum(_d(r["position_size"]) for r in result)

    if total_size > base and total_size > 0:
        scale = base / total_size
        for r in result:
            r["position_size"] *= scale

    return result


def common_calculate_rank_score(
    row: dict[str, Any],
    config: dict | None = None,
) -> tuple[Decimal, Decimal]:
    """
    Same as the raw_rank_score / adj_score calculation in the existing backtest_sizing.py.
    """

    final_score = _d(row.get("final_score"))
    flow = _d(row.get("flow_score"))
    tape = _d(row.get("tape_score"))
    info = _d(row.get("info_score"))
    vol = _d(row.get("volatility_20d"))

    if vol < 0:
        vol = Decimal("0")

    positive_flow = flow if flow > 0 else Decimal("0")
    positive_tape = tape if tape > 0 else Decimal("0")
    positive_info = info if info > 0 else Decimal("0")

    raw_rank_score = (
        final_score * _cfg_decimal(config, "final_weight", "0.65")
        + positive_flow * _cfg_decimal(config, "flow_weight", "0.25")
        + positive_tape * _cfg_decimal(config, "tape_weight", "0.10")
        + positive_info * _cfg_decimal(config, "info_bonus_weight", "0.05")
    )

    penalty = Decimal("1") + (
        vol * _cfg_decimal(config, "vol_penalty_multiplier", "16.0")
    )

    adj_score = raw_rank_score / penalty if penalty > 0 else raw_rank_score

    return raw_rank_score, adj_score


def common_allocation_sort_key(row: dict[str, Any]):
    """
    Same as the sort key in the existing backtest_sizing.py.

    Used with reverse=True:
    - highest adj_score first
    - highest final_score first
    - highest flow_score first
    """

    return (
        _d(row.get("adj_score")),
        _d(row.get("final_score")),
        _d(row.get("flow_score")),
    )


def _d(value: Any) -> Decimal:
    if value is None:
        return Decimal("0")
    return Decimal(str(value))


def _clamp(value: Decimal, min_value: Decimal, max_value: Decimal) -> Decimal:
    return max(min_value, min(value, max_value))


def _cfg_decimal(config: dict | None, key: str, default: str) -> Decimal:
    if not config:
        return Decimal(default)

    value = config.get(key)

    if value is None:
        return Decimal(default)

    return Decimal(str(value))

def common_apply_backtest_buy_size_haircut(
    size: float,
    guard: CommonGuardDecision,
    config: dict | None = None,
) -> tuple[float, dict[str, Any]]:
    """
    Same as the BUY toxic-flag-based size haircut in the existing backtest_buy_logic.py.

    Existing logic:
    - hot_chase                  → size *= 0.1
    - buy_day_stop_risk          → size *= 0.1
    - mid_flow_tight_range_risk  → size *= 0.1
    - flow_0_9_plus_soft         → size *= 0.70

    The priority also matches the existing elif order:
    hot_chase > buy_day_stop_risk > mid_flow_tight_range_risk > flow_0_9_plus_soft
    """

    original_size = float(size)
    adjusted_size = original_size

    flags = guard.detail.get("risk_flags", {}) if guard and guard.detail else {}

    hot_chase = bool(flags.get("is_hot_chase", flags.get("hot_chase", False)))
    buy_day_stop_risk = bool(
        flags.get("is_buy_day_stop_risk", flags.get("buy_day_stop_risk", False))
    )
    mid_flow_tight_range_risk = bool(
        flags.get(
            "is_mid_flow_tight_range_risk",
            flags.get("mid_flow_tight_range_risk", False),
        )
    )
    flow_0_9_plus_soft = bool(
        flags.get("is_flow_0_9_plus_soft", flags.get("flow_0_9_plus_soft", False))
    )
    high_flow_high_score_soft = bool(
        flags.get(
            "is_high_flow_high_score_soft",
            flags.get("high_flow_high_score_soft", False),
        )
    )

    applied_reason = None
    multiplier = 1.0

    applied_reasons = []

    if hot_chase:
        multiplier = common_get_config_float(config, "hot_chase_size_multiplier", 0.10)
        applied_reason = "hot_chase"
        applied_reasons.append(applied_reason)
    elif buy_day_stop_risk:
        multiplier = common_get_config_float(config, "buy_day_stop_risk_size_multiplier", 0.10)
        applied_reason = "buy_day_stop_risk"
        applied_reasons.append(applied_reason)
    elif mid_flow_tight_range_risk:
        multiplier = common_get_config_float(config, "mid_flow_tight_range_size_multiplier", 0.10)
        applied_reason = "mid_flow_tight_range_risk"
        applied_reasons.append(applied_reason)
    elif flow_0_9_plus_soft:
        multiplier = common_get_config_float(config, "flow_0_9_plus_soft_size_multiplier", 0.70)
        applied_reason = "flow_0_9_plus_soft"
        applied_reasons.append(applied_reason)

    if high_flow_high_score_soft:
        multiplier *= common_get_config_float(
            config,
            "high_flow_high_score_size_multiplier",
            0.95,
        )
        applied_reasons.append("high_flow_high_score_soft")

    adjusted_size = original_size * multiplier

    if applied_reasons:
        applied_reason = "+".join(applied_reasons)

    return adjusted_size, {
        "original_size": original_size,
        "adjusted_size": adjusted_size,
        "multiplier": multiplier,
        "applied_reason": applied_reason,
        "applied_reasons": applied_reasons,
        "is_hot_chase": hot_chase,
        "is_buy_day_stop_risk": buy_day_stop_risk,
        "is_mid_flow_tight_range_risk": mid_flow_tight_range_risk,
        "is_flow_0_9_plus_soft": flow_0_9_plus_soft,
        "is_high_flow_high_score_soft": high_flow_high_score_soft,
    }


def common_build_backtest_buy_info(
    row: dict[str, Any],
    market_decision: CommonMarketDecision,
    guard: CommonGuardDecision,
    position_size: float,
) -> dict[str, Any]:
    """
    Helper that builds buy_info with the same structure as build_buy_info() + toxic flag storage in the existing backtest_buy_logic.py.
    """

    flags = guard.detail.get("risk_flags", {}) if guard and guard.detail else {}

    return {
        "score": common_safe_float(row.get("final_score"), 0.0),
        "flow": common_safe_float(row.get("flow_score"), 0.0),
        "info": common_safe_float(row.get("info_score"), 0.0),
        "tape": common_safe_float(row.get("tape_score"), 0.0),
        "short": common_safe_float(row.get("short_pressure_score"), 0.0),
        "vol": common_safe_float(row.get("volatility_20d"), 0.0),
        "intraday_range": common_safe_float(row.get("intraday_range"), 0.0),
        "has_info_flag": bool(row.get("has_info_flag", False)),
        "entry_market_signal": str(market_decision.market_signal),
        "position_size": position_size,
        "is_hot_chase": bool(flags.get("is_hot_chase", flags.get("hot_chase", False))),
        "is_buy_day_stop_risk": bool(
            flags.get("is_buy_day_stop_risk", flags.get("buy_day_stop_risk", False))
        ),
        "is_mid_flow_tight_range_risk": bool(
            flags.get(
                "is_mid_flow_tight_range_risk",
                flags.get("mid_flow_tight_range_risk", False),
            )
        ),
        "is_flow_0_9_plus_soft": bool(
            flags.get("is_flow_0_9_plus_soft", flags.get("flow_0_9_plus_soft", False))
        ),
        "is_high_flow_high_score_soft": bool(
            flags.get(
                "is_high_flow_high_score_soft",
                flags.get("high_flow_high_score_soft", False),
            )
        ),
    }
