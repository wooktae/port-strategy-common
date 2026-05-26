"""
Common Strategy Version

research / decision / execution이 동일한 전략 코어를 사용하는지 추적하기 위한 버전 정보.
"""

COMMON_STRATEGY_NAME = "PORT_COMMON_STRATEGY_CORE"

COMMON_STRATEGY_VERSION = "COMMON_STRATEGY_V1.0.0"

COMMON_STRATEGY_DESCRIPTION = (
    "Shared strategy core for backtest research, daily decision, and execution candidate generation."
)


def common_get_strategy_version() -> str:
    return COMMON_STRATEGY_VERSION


def common_get_strategy_name() -> str:
    return COMMON_STRATEGY_NAME


def common_get_strategy_metadata() -> dict:
    return {
        "strategy_name": COMMON_STRATEGY_NAME,
        "strategy_version": COMMON_STRATEGY_VERSION,
        "description": COMMON_STRATEGY_DESCRIPTION,
    }