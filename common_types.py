"""공통 전략 코어에서 사용하는 enum 정의.

시장 신호, 매매 신호, 주문 방향, 판단 상태, 포지션 상태, 실행 모드를 문자열 enum으로 제공한다.
enum 값은 저장 데이터와 consumer 분기 조건에 영향을 줄 수 있어 임의 변경하지 않는다.
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
