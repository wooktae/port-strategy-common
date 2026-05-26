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
    기존 backtest_buy_logic.py의 hot_chase 조건과 동일.

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
    기존 backtest_buy_logic.py의 buy_day_stop_risk 조건과 동일.

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
    기존 backtest_buy_logic.py의 mid_flow_tight_range_risk 조건과 동일.

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
    기존 backtest_buy_logic.py의 flow_0_9_plus_soft 조건과 동일.

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
    고수급/고점수 과열 구간 미세 sizing haircut 실험용 flag.

    조건:
        flow_score >= 0.90
        and final_score >= 0.60

    주의:
    - BUY 차단용이 아님.
    - 기존 hot_chase / buy_day_stop_risk / flow_0_9_plus_soft를 대체하지 않음.
    - sizing 단계에서 기존 haircut 이후 추가 미세 multiplier로만 사용.
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
    BUY 후보 toxic flag 공통 판단.

    기존 backtest_buy_logic.py에서 buy_info에 저장하던 flag와 이름을 맞춤:
    - is_hot_chase
    - is_buy_day_stop_risk
    - is_mid_flow_tight_range_risk
    - is_flow_0_9_plus_soft

    주의:
    - 여기서는 BUY 차단 여부를 확정하지 않음.
    - size haircut 적용은 common_buy_sizing.py helper에서 처리 예정.
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

        # 기존 buy_info 저장명과 동일하게 추가 제공
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