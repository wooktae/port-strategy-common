from __future__ import annotations

from port_strategy_common.common_context import CommonPositionContext
from port_strategy_common.common_result import CommonMarketDecision, CommonSellDecision
from port_strategy_common.common_sell_guard import common_decide_sell_guard
from port_strategy_common.common_types import CommonTradeSignal


def common_decide_sell(
    position: CommonPositionContext,
    market: CommonMarketDecision,
    config: dict | None = None,
) -> CommonSellDecision:
    """
    SELL 최종 공통 판단 함수.

    단계:
    1. SELL guard/risk flag 계산
    2. 우선순위 기반 SELL/HOLD 결정

    주의:
    - DB 접근 없음
    - 주문 실행 없음
    - Backtest / Daily가 같은 입력을 주면 같은 결과를 반환해야 함
    """

    guard = common_decide_sell_guard(
        position=position,
        market=market,
        config=config,
    )

    flags = guard.detail.get("sell_flags", {})
    active_reasons = guard.detail.get("active_reasons", [])

    # 1. 강제 손절 계열은 최소 보유일보다 우선
    if flags.get("hard_stop"):
        return _common_build_sell_decision(
            position=position,
            market=market,
            guard_detail=guard.detail,
            reason="SELL_HARD_STOP",
            priority=1,
        )

    if flags.get("intraday_stop"):
        return _common_build_sell_decision(
            position=position,
            market=market,
            guard_detail=guard.detail,
            reason="SELL_INTRADAY_STOP",
            priority=2,
        )

    # 2. 이익 보호
    if flags.get("profit_protect"):
        return _common_build_sell_decision(
            position=position,
            market=market,
            guard_detail=guard.detail,
            reason="SELL_PROFIT_PROTECT",
            priority=3,
        )

    # 3. 초기 리스크 컷
    if flags.get("early_risk_cut"):
        return _common_build_sell_decision(
            position=position,
            market=market,
            guard_detail=guard.detail,
            reason="SELL_EARLY_RISK_CUT",
            priority=4,
        )

    if flags.get("early_cut"):
        return _common_build_sell_decision(
            position=position,
            market=market,
            guard_detail=guard.detail,
            reason="SELL_EARLY_CUT",
            priority=5,
        )

    # 4. 최소 보유일 보호
    if flags.get("min_holding_days"):
        return _common_build_hold_decision(
            position=position,
            market=market,
            guard_detail=guard.detail,
            reason="HOLD_MIN_HOLDING_DAYS",
            priority=10,
        )

    # 5. MARKET BLOCK 유지 허용
    if flags.get("market_block") and flags.get("market_block_keep_allowed"):
        return _common_build_hold_decision(
            position=position,
            market=market,
            guard_detail=guard.detail,
            reason="HOLD_MARKET_BLOCK_KEEP_ALLOWED",
            priority=20,
        )

    # 6. MARKET BLOCK 위험 계열
    if flags.get("market_block_quality_drop"):
        return _common_build_sell_decision(
            position=position,
            market=market,
            guard_detail=guard.detail,
            reason="SELL_MARKET_BLOCK_QUALITY_DROP",
            priority=30,
        )

    if flags.get("market_block_both_weak"):
        return _common_build_sell_decision(
            position=position,
            market=market,
            guard_detail=guard.detail,
            reason="SELL_MARKET_BLOCK_BOTH_WEAK",
            priority=31,
        )

    if flags.get("market_block_flow_only_weak"):
        return _common_build_sell_decision(
            position=position,
            market=market,
            guard_detail=guard.detail,
            reason="SELL_MARKET_BLOCK_FLOW_ONLY_WEAK",
            priority=32,
        )

    if flags.get("market_block_mid_hold_neither_clear"):
        return _common_build_sell_decision(
            position=position,
            market=market,
            guard_detail=guard.detail,
            reason="SELL_MARKET_BLOCK_MID_HOLD_NEITHER_CLEAR",
            priority=33,
        )

    # 7. 일반 약세 계열
    if flags.get("stale_loser"):
        return _common_build_sell_decision(
            position=position,
            market=market,
            guard_detail=guard.detail,
            reason="SELL_STALE_LOSER",
            priority=40,
        )

    if flags.get("flow_breakdown"):
        return _common_build_sell_decision(
            position=position,
            market=market,
            guard_detail=guard.detail,
            reason="SELL_FLOW_BREAKDOWN",
            priority=41,
        )

    if flags.get("score_breakdown"):
        return _common_build_sell_decision(
            position=position,
            market=market,
            guard_detail=guard.detail,
            reason="SELL_SCORE_BREAKDOWN",
            priority=42,
        )

    # 8. 최대 보유일
    if flags.get("max_holding_days"):
        return _common_build_sell_decision(
            position=position,
            market=market,
            guard_detail=guard.detail,
            reason="SELL_MAX_HOLDING_DAYS",
            priority=50,
        )

    # 9. 기본 HOLD
    return _common_build_hold_decision(
        position=position,
        market=market,
        guard_detail=guard.detail,
        reason="HOLD_NO_SELL_SIGNAL",
        priority=999,
        active_reasons=active_reasons,
    )


def _common_build_sell_decision(
    *,
    position: CommonPositionContext,
    market: CommonMarketDecision,
    guard_detail: dict,
    reason: str,
    priority: int,
) -> CommonSellDecision:
    return CommonSellDecision(
        signal=CommonTradeSignal.SELL.value,
        should_sell=True,
        reason=reason,
        detail={
            "ticker_code": position.ticker_code,
            "ticker_name": position.ticker_name,
            "current_date": position.current_date,
            "entry_date": position.entry_date,
            "holding_days": position.holding_days,
            "cum_return": position.cum_return,
            "market_signal": market.market_signal,
            "priority": priority,
            "guard": guard_detail,
        },
    )


def _common_build_hold_decision(
    *,
    position: CommonPositionContext,
    market: CommonMarketDecision,
    guard_detail: dict,
    reason: str,
    priority: int,
    active_reasons: list[str] | None = None,
) -> CommonSellDecision:
    return CommonSellDecision(
        signal=CommonTradeSignal.HOLD.value,
        should_sell=False,
        reason=reason,
        detail={
            "ticker_code": position.ticker_code,
            "ticker_name": position.ticker_name,
            "current_date": position.current_date,
            "entry_date": position.entry_date,
            "holding_days": position.holding_days,
            "cum_return": position.cum_return,
            "market_signal": market.market_signal,
            "priority": priority,
            "active_reasons": active_reasons or guard_detail.get("active_reasons", []),
            "guard": guard_detail,
        },
    )

# =========================================================
# Backtest 기존 evaluate_sell()과 1:1 동일한 함수
# =========================================================

from port_strategy_common.config import SELL_CONFIG
from port_strategy_common.common_utils import common_safe_float


_BACKTEST_SELL_CFG = SELL_CONFIG


def common_evaluate_backtest_sell(
    pos,
    feature,
    decision,
    raw_today_ret,
    today_ret,
    config: dict | None = None,
) -> dict:
    """
    기존 port_strategy_research.backtest_sell_logic.evaluate_sell()과
    1:1 동일한 결과를 반환하기 위한 Backtest 전용 SELL 판단 함수.

    주의:
    - 기존 sell_reason 문자열 유지
    - 기존 반환 dict key 유지
    - 기존 비교 연산자(<, <=, ==) 유지
    - 기존 BLOCK 세부 flag 유지
    """

    cfg = config or _BACKTEST_SELL_CFG

    market_block_strong_min_flow = float(cfg["market_block_strong_min_flow"])
    market_block_strong_min_final = float(cfg["market_block_strong_min_final"])
    market_block_strong_keep_profit = float(cfg["market_block_strong_keep_profit"])
    market_block_quality_drop_flow = float(cfg["market_block_quality_drop_flow"])
    market_block_quality_drop_final = float(cfg["market_block_quality_drop_final"])
    market_block_early_max_holding_days = int(cfg["market_block_early_max_holding_days"])
    market_block_flat_min_cum_return = float(cfg["market_block_flat_min_cum_return"])
    market_block_both_weak_flow = float(cfg["market_block_both_weak_flow"])
    market_block_both_weak_final = float(cfg["market_block_both_weak_final"])
    market_block_both_weak_min_holding_days = int(cfg["market_block_both_weak_min_holding_days"])

    market_block_mid_hold_neither_clear_min_holding_days = int(
        cfg["market_block_mid_hold_neither_clear_min_holding_days"]
    )
    market_block_mid_hold_neither_clear_max_holding_days = int(
        cfg["market_block_mid_hold_neither_clear_max_holding_days"]
    )
    market_block_mid_hold_neither_clear_max_flow = float(
        cfg["market_block_mid_hold_neither_clear_max_flow"]
    )
    market_block_mid_hold_neither_clear_max_final = float(
        cfg["market_block_mid_hold_neither_clear_max_final"]
    )

    market_block_flow_only_weak_max_holding_days = int(
        cfg["market_block_flow_only_weak_max_holding_days"]
    )
    market_block_flow_only_weak_max_flow = float(
        cfg["market_block_flow_only_weak_max_flow"]
    )
    market_block_flow_only_weak_max_final = float(
        cfg["market_block_flow_only_weak_max_final"]
    )

    market_block_high_flow_neither_clear_min_holding_days = int(
        cfg["market_block_high_flow_neither_clear_min_holding_days"]
    )
    market_block_high_flow_neither_clear_max_holding_days = int(
        cfg["market_block_high_flow_neither_clear_max_holding_days"]
    )
    market_block_high_flow_neither_clear_min_flow = float(
        cfg["market_block_high_flow_neither_clear_min_flow"]
    )
    market_block_high_flow_neither_clear_min_final = float(
        cfg["market_block_high_flow_neither_clear_min_final"]
    )

    block_survivor_only_holding_day = int(cfg["block_survivor_only_holding_day"])
    block_survivor_min_flow = float(cfg["block_survivor_min_flow"])
    block_survivor_min_final = float(cfg["block_survivor_min_final"])
    block_survivor_min_cum_return = float(cfg["block_survivor_min_cum_return"])

    market_block_mid_survivor_min_holding_days = int(
        cfg["market_block_mid_survivor_min_holding_days"]
    )
    market_block_mid_survivor_max_holding_days = int(
        cfg["market_block_mid_survivor_max_holding_days"]
    )
    market_block_mid_survivor_min_flow = float(
        cfg["market_block_mid_survivor_min_flow"]
    )
    market_block_mid_survivor_min_final = float(
        cfg["market_block_mid_survivor_min_final"]
    )
    market_block_mid_survivor_min_cum_return = float(
        cfg["market_block_mid_survivor_min_cum_return"]
    )
    market_block_mid_survivor_min_raw_today_return = float(
        cfg["market_block_mid_survivor_min_raw_today_return"]
    )

    flow = common_safe_float(feature.get("flow_score"), 0.0)
    final_score = common_safe_float(feature.get("final_score"), 0.0)
    short = common_safe_float(feature.get("short_pressure_score"), 0.0)

    raw_today_ret = common_safe_float(raw_today_ret, 0.0)
    today_ret = common_safe_float(today_ret, 0.0)

    prev_cum = common_safe_float(pos.get("cum_return", 0.0), 0.0)
    holding_days = int(pos.get("holding_days", 0)) + 1
    cum_return = ((1 + prev_cum) * (1 + today_ret)) - 1

    sell_flag = False
    sell_reason = ""

    required_keep_profit = None
    is_quality_drop = False
    is_flat_candidate = False
    is_both_weak = False
    is_mid_hold_neither_clear = False
    is_flow_only_weak = False
    is_high_flow_neither_clear = False
    is_block_survivor_candidate = False
    is_mid_hold_survivor_candidate = False

    if raw_today_ret <= float(cfg["hard_stop_daily_return"]):
        sell_flag = True
        sell_reason = "hard_stop"

    elif (
        cum_return > float(cfg["profit_protect_cum_return"])
        and raw_today_ret < float(cfg["profit_protect_daily_drop"])
    ):
        sell_flag = True
        sell_reason = "profit_protect"

    elif (
        holding_days <= cfg["early_risk_cut_max_holding_days"]
        and raw_today_ret <= float(cfg["early_risk_cut_daily_return"])
    ):
        sell_flag = True
        sell_reason = "early_risk_cut"

    elif holding_days == cfg["min_holding_days_no_sell"]:
        sell_flag = False

    elif holding_days == cfg["early_cut_holding_days"]:
        if cum_return <= float(cfg["early_cut_cum_return"]):
            sell_flag = True
            sell_reason = "early_cut"

    else:
        if decision.signal_type == "BLOCK":
            required_keep_profit = float(cfg["market_block_min_keep_profit"])

            if (
                flow >= market_block_strong_min_flow
                and final_score >= market_block_strong_min_final
            ):
                required_keep_profit = market_block_strong_keep_profit

            is_quality_drop = (
                flow < market_block_quality_drop_flow
                or final_score < market_block_quality_drop_final
            )

            is_both_weak = (
                flow < market_block_both_weak_flow
                and final_score < market_block_both_weak_final
            )

            is_flow_only_weak = (
                not is_quality_drop
                and not is_both_weak
                and holding_days <= market_block_flow_only_weak_max_holding_days
                and flow < market_block_flow_only_weak_max_flow
                and final_score < market_block_flow_only_weak_max_final
            )

            is_flat_candidate = (
                cum_return >= market_block_flat_min_cum_return
                and cum_return < required_keep_profit
                and not is_quality_drop
            )

            is_block_survivor_candidate = (
                not is_quality_drop
                and not is_both_weak
                and not is_flat_candidate
                and holding_days == block_survivor_only_holding_day
                and cum_return >= block_survivor_min_cum_return
                and flow >= block_survivor_min_flow
                and final_score >= block_survivor_min_final
            )

            is_high_flow_neither_clear = (
                not is_quality_drop
                and not is_flat_candidate
                and not is_both_weak
                and holding_days >= market_block_high_flow_neither_clear_min_holding_days
                and holding_days <= market_block_high_flow_neither_clear_max_holding_days
                and flow >= market_block_high_flow_neither_clear_min_flow
                and final_score >= market_block_high_flow_neither_clear_min_final
                and flow < market_block_mid_hold_neither_clear_max_flow
                and final_score < market_block_mid_hold_neither_clear_max_final
            )

            is_mid_hold_survivor_candidate = (
                not is_quality_drop
                and not is_flat_candidate
                and not is_both_weak
                and not is_flow_only_weak
                and holding_days >= market_block_mid_survivor_min_holding_days
                and holding_days <= market_block_mid_survivor_max_holding_days
                and cum_return >= market_block_mid_survivor_min_cum_return
                and raw_today_ret > market_block_mid_survivor_min_raw_today_return
                and flow >= market_block_mid_survivor_min_flow
                and final_score >= market_block_mid_survivor_min_final
            )

            is_mid_hold_neither_clear = (
                not is_quality_drop
                and not is_flat_candidate
                and not is_both_weak
                and not is_flow_only_weak
                and not is_mid_hold_survivor_candidate
                and holding_days >= market_block_mid_hold_neither_clear_min_holding_days
                and holding_days <= market_block_mid_hold_neither_clear_max_holding_days
                and flow < market_block_mid_hold_neither_clear_max_flow
                and final_score < market_block_mid_hold_neither_clear_max_final
            )

            if cfg["market_block_force_sell_negative"] and cum_return < 0:
                sell_flag = True
                sell_reason = "market_block_loser"

            elif (
                holding_days >= cfg["market_block_sell_min_holding_days"]
                and cum_return < required_keep_profit
            ):
                if is_block_survivor_candidate:
                    sell_flag = False

                elif (
                    is_both_weak
                    and holding_days >= market_block_both_weak_min_holding_days
                ):
                    sell_flag = True
                    sell_reason = "market_block_both_weak_fast"

                elif is_quality_drop:
                    sell_flag = True
                    sell_reason = "market_block_quality_drop"

                elif (
                    is_flat_candidate
                    and holding_days <= market_block_early_max_holding_days
                ):
                    sell_flag = True
                    sell_reason = "market_block_early_flat"

                elif (
                    is_flat_candidate
                    and holding_days > market_block_early_max_holding_days
                ):
                    sell_flag = True
                    sell_reason = "market_block_late_flat"

                elif is_mid_hold_survivor_candidate:
                    sell_flag = False
                    sell_reason = ""

                elif is_mid_hold_neither_clear:
                    sell_flag = True
                    sell_reason = "market_block_mid_hold_neither_clear"

                elif is_high_flow_neither_clear:
                    sell_flag = True
                    sell_reason = "market_block_high_flow_neither_clear"

                elif is_flow_only_weak:
                    sell_flag = True
                    sell_reason = "market_block_flow_only_weak"

                else:
                    sell_flag = True
                    sell_reason = "market_block_weak_other"

            elif (
                holding_days >= cfg["market_block_max_win_holding_days"]
                and cum_return < required_keep_profit
            ):
                sell_flag = True
                sell_reason = "market_block_time_exit"

        if not sell_flag and holding_days >= cfg["max_holding_days"]:
            sell_flag = True
            sell_reason = "max_holding"

        if (
            not sell_flag
            and holding_days >= cfg["stale_loser_min_holding_days"]
            and cum_return <= float(cfg["stale_loser_cum_return"])
            and flow < float(cfg["stale_loser_flow"])
        ):
            sell_flag = True
            sell_reason = "stale_loser"

        if not sell_flag and short > float(cfg["sell_short_pressure"]):
            sell_flag = True
            sell_reason = "short_pressure"

        if (
            not sell_flag
            and holding_days >= cfg["flow_breakdown_min_holding_days"]
            and flow < float(cfg["sell_flow_breakdown"])
            and cum_return <= float(cfg["flow_breakdown_max_cum_return"])
        ):
            sell_flag = True
            sell_reason = "flow_breakdown"

        if (
            not sell_flag
            and holding_days >= cfg["score_breakdown_min_holding_days"]
            and final_score < float(cfg["sell_final_breakdown"])
            and cum_return <= float(cfg["score_breakdown_max_cum_return"])
        ):
            sell_flag = True
            sell_reason = "score_breakdown"

        if (
            not sell_flag
            and holding_days >= cfg["weak_signal_min_holding_days"]
            and flow < float(cfg["sell_weak_flow"])
            and final_score < float(cfg["sell_weak_final"])
            and cum_return <= float(cfg["weak_signal_max_cum_return"])
        ):
            sell_flag = True
            sell_reason = "weak_signal"

    return {
        "sell_flag": sell_flag,
        "sell_reason": sell_reason,
        "holding_days": holding_days,
        "cum_return": cum_return,
        "flow": flow,
        "final_score": final_score,
        "short": short,
        "raw_today_ret": raw_today_ret,
        "today_ret": today_ret,
        "required_keep_profit": required_keep_profit
        if decision.signal_type == "BLOCK"
        else None,
        "is_quality_drop": is_quality_drop
        if decision.signal_type == "BLOCK"
        else False,
        "is_flat_candidate": is_flat_candidate
        if decision.signal_type == "BLOCK"
        else False,
        "is_both_weak": is_both_weak
        if decision.signal_type == "BLOCK"
        else False,
        "is_mid_hold_neither_clear": is_mid_hold_neither_clear
        if decision.signal_type == "BLOCK"
        else False,
        "is_flow_only_weak": is_flow_only_weak
        if decision.signal_type == "BLOCK"
        else False,
        "is_high_flow_neither_clear": is_high_flow_neither_clear
        if decision.signal_type == "BLOCK"
        else False,
        "is_block_survivor_candidate": is_block_survivor_candidate
        if decision.signal_type == "BLOCK"
        else False,
        "is_mid_hold_survivor_candidate": is_mid_hold_survivor_candidate
        if decision.signal_type == "BLOCK"
        else False,
    }
