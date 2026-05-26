"""
port_strategy_common

Shared Strategy Core package.

현재 구조:
- 기존 legacy 모듈 유지: utils.py, config.py, run_store.py
- 신규 common_* 모듈 추가 예정
- research / decision / execution이 공통 전략 판단 로직을 재사용하기 위한 패키지

원칙:
1. common_* 파일은 DB 접근 금지
2. common_* 파일은 HTTP/API 호출 금지
3. common_* 파일은 파일 IO 금지
4. common_* 파일은 입력 context + config 기반 순수 함수 중심
"""

from port_strategy_common.common_version import (
    COMMON_STRATEGY_DESCRIPTION,
    COMMON_STRATEGY_NAME,
    COMMON_STRATEGY_VERSION,
    common_get_strategy_metadata,
    common_get_strategy_name,
    common_get_strategy_version,
)

__all__ = [
    "COMMON_STRATEGY_DESCRIPTION",
    "COMMON_STRATEGY_NAME",
    "COMMON_STRATEGY_VERSION",
    "common_get_strategy_metadata",
    "common_get_strategy_name",
    "common_get_strategy_version",
]