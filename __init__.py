"""
port_strategy_common

Shared Strategy Core package.

Current structure:
- Existing legacy modules retained: utils.py, config.py
- New common_* modules planned for addition
- Package for research / decision / execution to reuse shared strategy decision logic

Principles:
1. common_* files must not access the DB
2. common_* files must not make HTTP/API calls
3. common_* files must not perform file IO
4. common_* files are centered on pure functions based on input context + config
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
