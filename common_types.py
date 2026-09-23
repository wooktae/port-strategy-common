"""Enum definitions used by the shared strategy core.

Provides market signal, trade signal, order side, decision status, position status, and execution mode as string enums.
Enum values can affect stored data and consumer branching conditions, so do not change them arbitrarily.
"""

from enum import Enum


class CommonMarketSignal(str, Enum):
    BLOCK = "BLOCK"
    DEFENSIVE = "DEFENSIVE"
    NEUTRAL = "NEUTRAL"
    AGGRESSIVE = "AGGRESSIVE"


class CommonTradeSignal(str, Enum):
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"
    SKIP = "SKIP"


class CommonOrderSide(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


class CommonDecisionStatus(str, Enum):
    PASSED = "PASSED"
    BLOCKED = "BLOCKED"
    SKIPPED = "SKIPPED"


class CommonPositionStatus(str, Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    PARTIALLY_CLOSED = "PARTIALLY_CLOSED"


class CommonExecutionMode(str, Enum):
    DRY_RUN = "DRY_RUN"
    MANUAL_TEST = "MANUAL_TEST"
    PAPER = "PAPER"
    LIVE = "LIVE"
