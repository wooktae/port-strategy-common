"""Common module for market regime decisions.

Takes a market context and config to compute the market signal, exposure, maximum position count, and minimum score criteria.
Following the common strategy module principle, it does not perform DB access, external API calls, or file IO.
"""

from __future__ import annotations

from port_strategy_common.common_context import CommonMarketContext
from port_strategy_common.common_result import CommonMarketDecision
from port_strategy_common.common_types import CommonMarketSignal
from port_strategy_common.common_utils import (
    common_get_config_float,
    common_get_config_int,
)


def common_decide_market(
    context: CommonMarketContext,
    config: dict | None = None,
) -> CommonMarketDecision:
    """
    Common market decision function for Backtest / Daily.

    Same flow as the existing backtest_market.evaluate_market() logic:
    1. Determine the base signal from market_regime_score
    2. Downgrade based on weak breadth
    3. Downgrade based on weak flow
    4. Downgrade based on weak macro
    5. Determine exposure / max_positions / min_score / min_flow per signal
    6. Override exposure when the AGGRESSIVE + strong_breadth_confirm condition holds
    """
    market_score = context.market_regime_score
    breadth = context.breadth_pressure_score
    flow = context.flow_pressure_score
    macro = context.macro_pressure_score

    block_threshold = common_get_config_float(
        config,
        "block_market_regime_score",
        -0.11,
    )
    defensive_threshold = common_get_config_float(
        config,
        "defensive_market_regime_score",
        -0.06,
    )
    aggressive_threshold = common_get_config_float(
        config,
        "aggressive_market_regime_score",
        0.05,
    )

    if market_score < block_threshold:
        signal = CommonMarketSignal.BLOCK.value
        reason = "market_score_block"
    elif market_score < defensive_threshold:
        signal = CommonMarketSignal.DEFENSIVE.value
        reason = "market_score_defensive"
    elif market_score < aggressive_threshold:
        signal = CommonMarketSignal.NEUTRAL.value
        reason = "market_score_neutral"
    else:
        signal = CommonMarketSignal.AGGRESSIVE.value
        reason = "market_score_aggressive"

    very_weak_breadth_score = common_get_config_float(
        config,
        "very_weak_breadth_score",
        -0.35,
    )
    weak_breadth_score = common_get_config_float(
        config,
        "weak_breadth_score",
        -0.20,
    )

    if breadth <= very_weak_breadth_score:
        signal = _common_downgrade_market_signal(
            _common_downgrade_market_signal(signal)
        )
        reason += "|very_weak_breadth"
    elif breadth <= weak_breadth_score:
        signal = _common_downgrade_market_signal(signal)
        reason += "|weak_breadth"

    very_weak_flow_score = common_get_config_float(
        config,
        "very_weak_flow_score",
        -0.80,
    )
    weak_flow_score = common_get_config_float(
        config,
        "weak_flow_score",
        -0.40,
    )

    if flow <= very_weak_flow_score:
        signal = _common_downgrade_market_signal(
            _common_downgrade_market_signal(signal)
        )
        reason += "|very_weak_flow"
    elif flow <= weak_flow_score:
        signal = _common_downgrade_market_signal(signal)
        reason += "|weak_flow"

    very_weak_macro_score = common_get_config_float(
        config,
        "very_weak_macro_score",
        -0.10,
    )
    weak_macro_score = common_get_config_float(
        config,
        "weak_macro_score",
        -0.05,
    )

    if macro <= very_weak_macro_score:
        signal = _common_downgrade_market_signal(signal)
        reason += "|very_weak_macro"
    elif macro <= weak_macro_score and signal == CommonMarketSignal.AGGRESSIVE.value:
        signal = CommonMarketSignal.NEUTRAL.value
        reason += "|weak_macro"

    exposure_override = None

    if signal == CommonMarketSignal.AGGRESSIVE.value:
        strong_breadth_score = common_get_config_float(
            config,
            "strong_breadth_score",
            0.15,
        )
        strong_breadth_confirm_min_flow = common_get_config_float(
            config,
            "strong_breadth_confirm_min_flow",
            0.00,
        )

        if breadth >= strong_breadth_score and flow >= strong_breadth_confirm_min_flow:
            exposure_override = common_get_config_float(
                config,
                "strong_breadth_confirm_exposure",
                0.80,
            )
            reason += "|strong_breadth_confirm"

    return _common_build_market_decision(
        market_signal=signal,
        reason=reason,
        config=config,
        prefix=signal.lower(),
        context=context,
        exposure_override=exposure_override,
    )


def _common_downgrade_market_signal(signal: str) -> str:
    if signal == CommonMarketSignal.AGGRESSIVE.value:
        return CommonMarketSignal.NEUTRAL.value
    if signal == CommonMarketSignal.NEUTRAL.value:
        return CommonMarketSignal.DEFENSIVE.value
    return CommonMarketSignal.BLOCK.value


def _common_build_market_decision(
    *,
    market_signal: str,
    reason: str,
    config: dict | None,
    prefix: str,
    context: CommonMarketContext,
    exposure_override: float | None = None,
) -> CommonMarketDecision:
    base_exposure = (
        exposure_override
        if exposure_override is not None
        else common_get_config_float(
            config,
            f"{prefix}_exposure",
            _common_default_exposure(prefix),
        )
    )

    max_positions = common_get_config_int(
        config,
        f"{prefix}_max_positions",
        _common_default_max_positions(prefix),
    )
    min_score = common_get_config_float(
        config,
        f"{prefix}_min_score",
        _common_default_min_score(prefix),
    )
    min_flow = common_get_config_float(
        config,
        f"{prefix}_min_flow",
        _common_default_min_flow(prefix),
    )

    return CommonMarketDecision(
        market_signal=market_signal,
        base_exposure=base_exposure,
        max_positions=max_positions,
        min_score=min_score,
        min_flow=min_flow,
        reason=reason,
        detail={
            "trade_date": context.trade_date,
            "market_regime_score": context.market_regime_score,
            "breadth_pressure_score": context.breadth_pressure_score,
            "flow_pressure_score": context.flow_pressure_score,
            "macro_pressure_score": context.macro_pressure_score,
            "program_pressure_score": context.program_pressure_score,
            "prefix": prefix,
            "exposure_override": exposure_override,
        },
    )


def _common_default_exposure(prefix: str) -> float:
    defaults = {
        "block": 0.0,
        "defensive": 0.20,
        "neutral": 0.40,
        "aggressive": 0.70,
    }
    return defaults.get(prefix, 0.0)


def _common_default_max_positions(prefix: str) -> int:
    defaults = {
        "block": 0,
        "defensive": 2,
        "neutral": 2,
        "aggressive": 4,
    }
    return defaults.get(prefix, 0)


def _common_default_min_score(prefix: str) -> float:
    defaults = {
        "block": 1.00,
        "defensive": 0.08,
        "neutral": 0.085,
        "aggressive": 0.05,
    }
    return defaults.get(prefix, 1.00)


def _common_default_min_flow(prefix: str) -> float:
    defaults = {
        "block": 1.00,
        "defensive": 0.00,
        "neutral": 0.00,
        "aggressive": 0.00,
    }
    return defaults.get(prefix, 1.00)
