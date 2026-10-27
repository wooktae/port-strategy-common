"""Common module for buy-side risk guards.

Computes the flags needed for BUY sizing, such as overheated chasing, buy-day stop-loss risk, and mid-flow/tight-range risk.
This module uses only the input context and config, without order execution or DB storage.
"""

from __future__ import annotations

from port_strategy_common.common_context import CommonStockContext
from port_strategy_common.common_result import CommonGuardDecision, CommonMarketDecision
from port_strategy_common.common_types import CommonMarketSignal
from port_strategy_common.common_utils import common_get_config_float, common_safe_float


def common_is_hot_chase(
    stock: CommonStockContext,
    market: CommonMarketDecision,
    config: dict | None = None,
) -> bool:
    """
    Same as the hot_chase condition in the existing backtest_buy_logic.py.

    hot_chase =
        AGGRESSIVE
        and flow >= 0.90
        and score >= 0.60
        and intraday_range >= 0.05
        and vol < 0.04
    """

    flow_min = common_get_config_float(config, "hot_chase_flow_min", 0.90)
    score_min = common_get_config_float(config, "hot_chase_score_min", 0.60)
    intraday_min = common_get_config_float(config, "hot_chase_intraday_min", 0.05)
    vol_max = common_get_config_float(config, "hot_chase_vol_max", 0.04)

    return (
        market.market_signal == CommonMarketSignal.AGGRESSIVE.value
        and stock.flow_pressure_score >= flow_min
        and stock.final_score >= score_min
        and common_safe_float(stock.intraday_range, 0.0) >= intraday_min
        and stock.volatility_score < vol_max
    )


def common_is_buy_day_stop_risk(
    stock: CommonStockContext,
    config: dict | None = None,
) -> bool:
    """
    Same as the buy_day_stop_risk condition in the existing backtest_buy_logic.py.

    buy_day_stop_risk =
        flow >= 0.85
        and score >= 0.60
        and intraday_range >= 0.07
        and vol < 0.035
    """

    flow_min = common_get_config_float(config, "buy_day_stop_risk_flow_min", 0.85)
    score_min = common_get_config_float(config, "buy_day_stop_risk_score_min", 0.60)
    intraday_min = common_get_config_float(config, "buy_day_stop_risk_intraday_min", 0.07)
    vol_max = common_get_config_float(config, "buy_day_stop_risk_vol_max", 0.035)

    return (
        stock.flow_pressure_score >= flow_min
        and stock.final_score >= score_min
        and common_safe_float(stock.intraday_range, 0.0) >= intraday_min
        and stock.volatility_score < vol_max
    )


def common_is_mid_flow_tight_range_risk(
    stock: CommonStockContext,
    *,
    hot_chase: bool,
    buy_day_stop_risk: bool,
    config: dict | None = None,
) -> bool:
    """
    Same as the mid_flow_tight_range_risk condition in the existing backtest_buy_logic.py.

    mid_flow_tight_range_risk =
        not hot_chase
        and not buy_day_stop_risk
        and flow >= 0.75
        and flow < 0.85
        and vol >= 0.025
        and intraday_range < 0.04
    """

    flow_min = common_get_config_float(config, "mid_flow_tight_range_flow_min", 0.75)
    flow_max = common_get_config_float(config, "mid_flow_tight_range_flow_max", 0.85)
    vol_min = common_get_config_float(config, "mid_flow_tight_range_vol_min", 0.025)
    intraday_max = common_get_config_float(config, "mid_flow_tight_range_intraday_max", 0.04)

    return (
        not hot_chase
        and not buy_day_stop_risk
        and stock.flow_pressure_score >= flow_min
        and stock.flow_pressure_score < flow_max
        and stock.volatility_score >= vol_min
        and common_safe_float(stock.intraday_range, 0.0) < intraday_max
    )


def common_is_flow_0_9_plus_soft(
    stock: CommonStockContext,
    market: CommonMarketDecision,
    *,
    hot_chase: bool,
    config: dict | None = None,
) -> bool:
    """
    Same as the flow_0_9_plus_soft condition in the existing backtest_buy_logic.py.

    flow_0_9_plus_soft =
        AGGRESSIVE
        and not hot_chase
        and flow >= 0.90
    """

    flow_min = common_get_config_float(config, "flow_0_9_plus_soft_min", 0.90)

    return (
        market.market_signal == CommonMarketSignal.AGGRESSIVE.value
        and not hot_chase
        and stock.flow_pressure_score >= flow_min
    )

def common_is_high_flow_high_score_soft(
    stock: CommonStockContext,
    config: dict | None = None,
) -> bool:
    """
    Experimental flag for a fine sizing haircut in the high-flow/high-score overheated zone.

    Condition:
        flow_score >= 0.90
        and final_score >= 0.60

    Note:
    - Not for blocking BUY.
    - Does not replace the existing hot_chase / buy_day_stop_risk / flow_0_9_plus_soft.
    - Used only as an additional fine multiplier after the existing haircut in the sizing stage.
    """

    enabled = bool(common_get_config_float(config, "high_flow_high_score_soft_enabled", 1.0))
    if not enabled:
        return False

    flow_min = common_get_config_float(config, "high_flow_high_score_flow_min", 0.90)
    final_min = common_get_config_float(config, "high_flow_high_score_final_min", 0.60)

    return (
        stock.flow_pressure_score >= flow_min
        and stock.final_score >= final_min
    )


def common_decide_buy_guard(
    stock: CommonStockContext,
    market: CommonMarketDecision,
    config: dict | None = None,
) -> CommonGuardDecision:
    """
    Common evaluation of BUY candidate toxic flags.

    Names are aligned with the flags previously stored in buy_info in the existing backtest_buy_logic.py:
    - is_hot_chase
    - is_buy_day_stop_risk
    - is_mid_flow_tight_range_risk
    - is_flow_0_9_plus_soft

    Note:
    - This does not finalize whether BUY is blocked.
    - Size haircut application is handled by the common_buy_sizing.py helper.
    """

    hot_chase = common_is_hot_chase(
        stock=stock,
        market=market,
        config=config,
    )

    buy_day_stop_risk = common_is_buy_day_stop_risk(
        stock=stock,
        config=config,
    )

    mid_flow_tight_range_risk = common_is_mid_flow_tight_range_risk(
        stock=stock,
        hot_chase=hot_chase,
        buy_day_stop_risk=buy_day_stop_risk,
        config=config,
    )

    flow_0_9_plus_soft = common_is_flow_0_9_plus_soft(
        stock=stock,
        market=market,
        hot_chase=hot_chase,
        config=config,
    )

    high_flow_high_score_soft = common_is_high_flow_high_score_soft(
        stock=stock,
        config=config,
    )

    risk_flags = {
        "hot_chase": hot_chase,
        "buy_day_stop_risk": buy_day_stop_risk,
        "mid_flow_tight_range_risk": mid_flow_tight_range_risk,
        "flow_0_9_plus_soft": flow_0_9_plus_soft,
        "high_flow_high_score_soft": high_flow_high_score_soft,

        # Also provided under the same names used in the existing buy_info storage
        "is_hot_chase": hot_chase,
        "is_buy_day_stop_risk": buy_day_stop_risk,
        "is_mid_flow_tight_range_risk": mid_flow_tight_range_risk,
        "is_flow_0_9_plus_soft": flow_0_9_plus_soft,
        "is_high_flow_high_score_soft": high_flow_high_score_soft,
    }

    active_reasons = [
        key
        for key in (
            "hot_chase",
            "buy_day_stop_risk",
            "mid_flow_tight_range_risk",
            "flow_0_9_plus_soft",
            "high_flow_high_score_soft",
        )
        if risk_flags[key]
    ]

    if active_reasons:
        return CommonGuardDecision(
            passed=False,
            reason="BUY_GUARD_RISK_DETECTED",
            detail={
                "ticker_code": stock.ticker_code,
                "ticker_name": stock.ticker_name,
                "market_signal": market.market_signal,
                "active_reasons": active_reasons,
                "risk_flags": risk_flags,
                "final_score": stock.final_score,
                "flow_pressure_score": stock.flow_pressure_score,
                "tape_score": stock.tape_score,
                "short_pressure_score": stock.short_pressure_score,
                "volatility_score": stock.volatility_score,
                "intraday_range": stock.intraday_range,
                "change_rate": stock.change_rate,
            },
        )

    return CommonGuardDecision(
        passed=True,
        reason="BUY_GUARD_PASSED",
        detail={
            "ticker_code": stock.ticker_code,
            "ticker_name": stock.ticker_name,
            "market_signal": market.market_signal,
            "active_reasons": [],
            "risk_flags": risk_flags,
            "final_score": stock.final_score,
            "flow_pressure_score": stock.flow_pressure_score,
            "tape_score": stock.tape_score,
            "short_pressure_score": stock.short_pressure_score,
            "volatility_score": stock.volatility_score,
            "intraday_range": stock.intraday_range,
            "change_rate": stock.change_rate,
        },
    )
