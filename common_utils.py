"""Safe-conversion utilities used by the shared strategy modules.

Safely convert None, NaN, Decimal, and string inputs into float/int/str/bool values.
Contains only pure helpers that reduce repetitive defensive logic in the strategy decision modules.
"""

from __future__ import annotations

import math
from decimal import Decimal
from typing import Any


def common_is_null(value: Any) -> bool:
    if value is None:
        return True

    try:
        import pandas as pd

        return bool(pd.isna(value))
    except Exception:
        return False


def common_safe_float(value: Any, default: float = 0.0) -> float:
    if common_is_null(value):
        return default

    if isinstance(value, Decimal):
        return float(value)

    try:
        result = float(value)
    except Exception:
        return default

    if math.isnan(result) or math.isinf(result):
        return default

    return result


def common_safe_int(value: Any, default: int = 0) -> int:
    if common_is_null(value):
        return default

    try:
        return int(value)
    except Exception:
        return default


def common_safe_str(value: Any, default: str = "") -> str:
    if common_is_null(value):
        return default

    try:
        return str(value)
    except Exception:
        return default


def common_clamp(value: float, min_value: float, max_value: float) -> float:
    return max(min_value, min(value, max_value))


def common_get_config_value(config: dict | None, key: str, default: Any = None) -> Any:
    if not config:
        return default

    value = config.get(key)
    return default if value is None else value


def common_get_config_float(config: dict | None, key: str, default: float = 0.0) -> float:
    return common_safe_float(common_get_config_value(config, key, default), default)


def common_get_config_int(config: dict | None, key: str, default: int = 0) -> int:
    return common_safe_int(common_get_config_value(config, key, default), default)


def common_get_config_bool(config: dict | None, key: str, default: bool = False) -> bool:
    value = common_get_config_value(config, key, default)

    if isinstance(value, bool):
        return value

    if isinstance(value, str):
        return value.strip().lower() in ("true", "1", "yes", "y")

    return bool(value)


def common_to_float(value: Any, default: float = 0.0) -> float:
    """
    Compatibility function for the existing utils.to_float().
    In new common_* modules, prefer using common_safe_float().
    """
    return common_safe_float(value, default)
