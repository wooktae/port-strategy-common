"""전략 코어 기본 설정과 runtime config snapshot 모듈.

시장, 필터, sizing, 매수/매도, 리포트 설정 값을 dictionary로 제공한다.
runtime config snapshot은 전략 설정만 반환한다.
"""

from __future__ import annotations

from copy import deepcopy
from decimal import Decimal
from typing import Any


# =========================================================
# IMMUTABLE META
# =========================================================
STRATEGY_NAME = "strategy_ai"
ENGINE_VERSION = "RESEARCH_V3_EXIT_SOFTENED"
TRADING_DAYS_PER_YEAR = 252


BACKTEST_START_DATE = "2023-01-27"
DECISION_RUN_DATE = "2026-04-02"
RISK_FREE_RATE = 0.03


# =========================================================
# GENERAL CONFIG
# =========================================================
GENERAL_CONFIG = {
    "allow_reentry_after_sell_same_day": False,
    "use_return_floor": False,
    "return_floor": Decimal("-0.025"),
    "risk_off_trigger_daily_return": Decimal("-0.03"),
    "risk_off_exposure_multiplier": Decimal("0.5"),
}


# =========================================================
# MARKET CONFIG
# =========================================================
MARKET_CONFIG = {
    "block_market_regime_score": Decimal("-0.11"),
    "defensive_market_regime_score": Decimal("-0.06"),
    "aggressive_market_regime_score": Decimal("0.05"),
    "weak_breadth_score": Decimal("-0.20"),
    "very_weak_breadth_score": Decimal("-0.35"),
    "strong_breadth_score": Decimal("0.15"),
    "weak_flow_score": Decimal("-0.40"),
    "very_weak_flow_score": Decimal("-0.80"),
    "weak_macro_score": Decimal("-0.05"),
    "very_weak_macro_score": Decimal("-0.10"),
    "block_exposure": Decimal("0.00"),
    "block_max_positions": 0,
    "block_min_score": Decimal("1.00"),
    "block_min_flow": Decimal("1.00"),
    "defensive_exposure": Decimal("0.20"),
    "defensive_max_positions": 2,
    "defensive_min_score": Decimal("0.08"),
    "defensive_min_flow": Decimal("0.00"),
    "neutral_exposure": Decimal("0.40"),
    "neutral_max_positions": 2,
    "neutral_min_score": Decimal("0.085"),
    "neutral_min_flow": Decimal("0.00"),
    "aggressive_exposure": Decimal("0.70"),
    "aggressive_max_positions": 4,
    "aggressive_min_score": Decimal("0.05"),
    "aggressive_min_flow": Decimal("0.00"),
    "strong_breadth_confirm_min_flow": Decimal("0.00"),
    "strong_breadth_confirm_exposure": Decimal("0.80"),
}


# =========================================================
# FILTER CONFIG
# =========================================================
FILTER_CONFIG = {
    "max_short_pressure": Decimal("0.80"),
    "max_volatility_20d": Decimal("0.08"),
    "max_intraday_range": Decimal("0.15"),
    "flow_min": Decimal("0.62"),
    "flow_strong": Decimal("0.03"),
    "final_min": Decimal("0.070"),
    "final_strong": Decimal("0.08"),
    "final_extreme": Decimal("0.13"),
    "tape_min": Decimal("-0.15"),
    "info_min": Decimal("-0.10"),
}


# =========================================================
# SIZING CONFIG
# =========================================================
SIZING_CONFIG = {
    "max_position_size": Decimal("0.35"),
    "min_position_size": Decimal("0.05"),
    "final_weight": Decimal("0.65"),
    "flow_weight": Decimal("0.25"),
    "tape_weight": Decimal("0.10"),
    "info_bonus_weight": Decimal("0.05"),
    "vol_penalty_multiplier": Decimal("16.0"),

    # 고수급/고점수 과열 구간 미세 haircut 실험
    "high_flow_high_score_soft_enabled": False,
    "high_flow_high_score_flow_min": Decimal("0.90"),
    "high_flow_high_score_final_min": Decimal("0.60"),
    "high_flow_high_score_size_multiplier": Decimal("0.90"),
}


# =========================================================
# BUY CONFIG
# =========================================================
BUY_CONFIG = {
    "buy_day_intraday_stop_loss": Decimal("-0.10"),
}


# =========================================================
# SELL CONFIG
# =========================================================
SELL_CONFIG = {
    "existing_position_intraday_stop_loss": Decimal("-0.10"),
    "hard_stop_daily_return": Decimal("-0.12"),
    "profit_protect_cum_return": Decimal("0.07"),
    "profit_protect_daily_drop": Decimal("-0.04"),
    "early_risk_cut_max_holding_days": 2,
    "early_risk_cut_daily_return": Decimal("-0.08"),
    "min_holding_days_no_sell": 1,
    "early_cut_holding_days": 2,
    "early_cut_cum_return": Decimal("-0.07"),
    "max_holding_days": 15,
    "market_block_force_sell_negative": False,
    "market_block_sell_min_holding_days": 3,
    "market_block_max_win_holding_days": 8,
    "market_block_min_keep_profit": Decimal("0.021"),

    # BLOCK에서도 매우 강한 종목은 유지 최소 수익 기준 완화
    "market_block_strong_min_flow": Decimal("0.85"),
    "market_block_strong_min_final": Decimal("0.55"),
    "market_block_strong_keep_profit": Decimal("0.000"),

    # 실험 A: market_block_weak 정밀 완화
    "market_block_relax_min_holding_days": 4,
    "market_block_relax_max_holding_days": 5,
    "market_block_relax_min_flow": Decimal("0.80"),
    "market_block_relax_min_final": Decimal("0.50"),
    "market_block_relax_min_cum_return": Decimal("0.00"),

    "sell_short_pressure": Decimal("1.30"),
    "sell_flow_breakdown": Decimal("-0.10"),
    "sell_final_breakdown": Decimal("0.00"),
    "sell_weak_flow": Decimal("0.00"),
    "sell_weak_final": Decimal("0.03"),
    "stale_loser_min_holding_days": 4,
    "stale_loser_cum_return": Decimal("-0.02"),
    "stale_loser_flow": Decimal("-0.05"),
    "flow_breakdown_min_holding_days": 4,
    "flow_breakdown_max_cum_return": Decimal("0.02"),
    "score_breakdown_min_holding_days": 4,
    "score_breakdown_max_cum_return": Decimal("0.01"),
    "weak_signal_min_holding_days": 5,
    "weak_signal_max_cum_return": Decimal("0.01"),
    "block_survivor_min_flow": Decimal("0.80"),
    "block_survivor_min_final": Decimal("0.50"),
    "block_survivor_min_cum_return": Decimal("0.00"),
    "block_survivor_only_holding_day": 3,

    "market_block_quality_drop_flow": Decimal("0.20"),
    "market_block_quality_drop_final": Decimal("0.15"),
    "market_block_early_max_holding_days": 5,
    "market_block_flat_min_cum_return": Decimal("0.00"),

    "market_block_both_weak_flow": 0.40,
    "market_block_both_weak_final": 0.28,
    "market_block_both_weak_min_holding_days": 4,

    "market_block_mid_hold_neither_clear_min_holding_days": 4,
    "market_block_mid_hold_neither_clear_max_holding_days": 5,
    "market_block_mid_hold_neither_clear_max_flow": 0.95,
    "market_block_mid_hold_neither_clear_max_final": 0.60,

    "market_block_flow_only_weak_max_holding_days": 3,
    "market_block_flow_only_weak_max_flow": Decimal("0.45"),
    "market_block_flow_only_weak_max_final": Decimal("0.40"),

    "market_block_high_flow_neither_clear_min_holding_days": 4,
    "market_block_high_flow_neither_clear_max_holding_days": 5,
    "market_block_high_flow_neither_clear_min_flow": Decimal("0.90"),
    "market_block_high_flow_neither_clear_min_final": Decimal("0.55"),

    "market_block_mid_survivor_min_holding_days": 4,
    "market_block_mid_survivor_max_holding_days": 5,
    "market_block_mid_survivor_min_flow": Decimal("0.85"),
    "market_block_mid_survivor_min_final": Decimal("0.53"),
    "market_block_mid_survivor_min_cum_return": Decimal("-0.03"),
    "market_block_mid_survivor_min_raw_today_return": Decimal("-0.015"),
}

# =========================================================
# REPORT_CONFIG
# =========================================================
REPORT_CONFIG = {
    "file_prefix": {
        "summary": "01_요약_리포트",
        "timeline": "02_일자별_매매_리포트",
        "trade_detail": "03_거래_상세_리포트",
        "recommendation": "04_추천_리포트",
    },

    "entry_buckets": {
        "buy_flow": [0.75, 0.90],
        "buy_score": [0.30, 0.45, 0.60],
        "buy_short": [0.30, 0.80],
        "buy_vol": [0.04, 0.08],
        "buy_intraday_range": [0.05, 0.10],
    },

    "holding_buckets": {
        "signal_holding": [2, 5, 10, 15],
        "mbweak_holding": [3, 5, 8],
    },

    "mbweak": {
        "strong_candidate_min_flow": 0.65,
        "strong_candidate_min_final": 0.45,
        "profit_bucket_edges": [-0.05, -0.02, 0.00, 0.023],
        "holding_bucket_labels": ["3이하", "4~5", "6~8", "9+"],
        "profit_bucket_labels": ["< -5%", "-5% ~ -2%", "-2% ~ 0%", "0% ~ 2.3%", "2.3%+"],
        "example_limit": 10,
        "flow_bucket_edges": [0.30, 0.50, 0.70, 0.85],
        "final_bucket_edges": [0.15, 0.30, 0.45, 0.60],
    },

    "formatter": {
        "flow_very_strong": 0.90,
        "flow_strong": 0.75,
        "info_positive_strong": 0.20,
    },

    "recommendation": {
        "sharpe_good": 1.5,
        "sharpe_excellent": 2.0,
        "mdd_warning": -0.20,
        "spread_meaningful": 0.03,
        "info_flag_gap_meaningful": 0.02,
        "min_sample_for_warning": 5,
        "min_sample_for_overlap": 10,
        "mbweak_ratio_warning": 40.0,
    },

    "labels": {
        "exit_reason": {
            "market_block_early_flat": "BLOCK 초기 평탄형 청산",
            "market_block_late_flat": "BLOCK 후기 평탄형 청산",
            "market_block_quality_drop": "BLOCK 질 저하형 청산",
            "market_block_weak_other": "BLOCK 기타 약세형 청산",
            "market_block_both_weak_fast": "BLOCK 수급·점수 동시 약세형 청산",
            "market_block_flow_only_weak": "BLOCK 수급 약세형 청산",
            "market_block_mid_hold_neither_clear": "BLOCK 중기 혼합·불명확형 청산",
        },
        "combo_type": {
            "both_weak": "수급·점수 동시 약세형",
            "flow_only_weak": "수급 약세형",
            "final_only_weak": "점수 약세형",
            "neither_clear": "혼합·불명확형",
        },
    }
}

def _to_serializable(value: Any) -> Any:
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, dict):
        return {k: _to_serializable(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_to_serializable(v) for v in value]
    return value


def get_runtime_config() -> dict[str, Any]:
    return {
        "strategy_name": STRATEGY_NAME,
        "engine_version": ENGINE_VERSION,
        "trading_days_per_year": TRADING_DAYS_PER_YEAR,
        "backtest_start_date": BACKTEST_START_DATE,
        "decision_run_date": DECISION_RUN_DATE,
        "risk_free_rate": RISK_FREE_RATE,
        "general": deepcopy(GENERAL_CONFIG),
        "market": deepcopy(MARKET_CONFIG),
        "filter": deepcopy(FILTER_CONFIG),
        "sizing": deepcopy(SIZING_CONFIG),
        "buy": deepcopy(BUY_CONFIG),
        "sell": deepcopy(SELL_CONFIG),
    }


def get_config_snapshot() -> dict[str, Any]:
    return _to_serializable(get_runtime_config())
