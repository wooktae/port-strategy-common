"""
Common Strategy Version

Version information for tracking whether research / decision / execution use the same strategy core.
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