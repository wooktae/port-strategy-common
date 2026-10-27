"""Orchestration module for the final buy decision.

Calls BUY filter, BUY guard, and BUY sizing in order to produce the final BUY/SKIP result.
Keeps a pure-function flow so that backtest and daily obtain the same result for the same input.
"""

from __future__ import annotations

from port_strategy_common.common_buy_filter import common_decide_buy_filter
from port_strategy_common.common_buy_guard import common_decide_buy_guard
from port_strategy_common.common_buy_sizing import common_calculate_buy_sizing
from port_strategy_common.common_context import CommonStockContext
from port_strategy_common.common_result import CommonBuyDecision, CommonMarketDecision
from port_strategy_common.common_types import CommonTradeSignal


def common_decide_buy(
    stock: CommonStockContext,
    market: CommonMarketDecision,
    *,
    filter_config: dict | None = None,
    guard_config: dict | None = None,
    sizing_config: dict | None = None,
    available_cash: float,
    current_position_count: int = 0,
) -> CommonBuyDecision:
    """
    Common final BUY decision function.

    Stages:
    1. BUY base filter
    2. BUY guard/risk flag
    3. BUY sizing
    4. Final BUY/SKIP decision

    Note:
    - No DB access
    - No order execution
    - Must return the same result when Backtest / Daily provide the same input
    """

    filter_decision = common_decide_buy_filter(
        stock=stock,
        market=market,
        config=filter_config,
    )

    if not filter_decision.passed:
        return CommonBuyDecision(
            signal=CommonTradeSignal.SKIP.value,
            passed=False,
            score=stock.final_score,
            target_weight=0.0,
            target_amount=0.0,
            target_qty=0,
            reason=filter_decision.reason,
            detail={
                "ticker_code": stock.ticker_code,
                "ticker_name": stock.ticker_name,
                "stage": "FILTER",
                "filter": filter_decision.detail,
            },
        )

    guard_decision = common_decide_buy_guard(
        stock=stock,
        market=market,
        config=guard_config,
    )

    sizing_decision = common_calculate_buy_sizing(
        stock=stock,
        market=market,
        guard=guard_decision,
        config=sizing_config,
        available_cash=available_cash,
        current_position_count=current_position_count,
    )

    if sizing_decision.target_qty <= 0:
        return CommonBuyDecision(
            signal=CommonTradeSignal.SKIP.value,
            passed=False,
            score=stock.final_score,
            target_weight=sizing_decision.target_weight,
            target_amount=sizing_decision.target_amount,
            target_qty=sizing_decision.target_qty,
            reason=sizing_decision.reason,
            detail={
                "ticker_code": stock.ticker_code,
                "ticker_name": stock.ticker_name,
                "stage": "SIZING",
                "filter": filter_decision.detail,
                "guard": guard_decision.detail,
                "sizing": sizing_decision.detail,
            },
        )

    return CommonBuyDecision(
        signal=CommonTradeSignal.BUY.value,
        passed=True,
        score=stock.final_score,
        target_weight=sizing_decision.target_weight,
        target_amount=sizing_decision.target_amount,
        target_qty=sizing_decision.target_qty,
        reason="BUY_PASSED",
        detail={
            "ticker_code": stock.ticker_code,
            "ticker_name": stock.ticker_name,
            "stage": "BUY",
            "market_signal": market.market_signal,
            "filter": filter_decision.detail,
            "guard": guard_decision.detail,
            "sizing": sizing_decision.detail,
        },
    )
