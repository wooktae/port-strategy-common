"""legacy utility 모듈.

기존 consumer 호환을 위해 `to_float` helper를 유지한다.
신규 common_* 모듈에서는 `common_utils.common_safe_float` 사용을 우선한다.
"""

from decimal import Decimal
import pandas as pd


def to_float(value, default=0.0):
    if value is None:
        return default
    if isinstance(value, Decimal):
        return float(value)
    try:
        if pd.isna(value):
            return default
    except Exception:
        pass
    try:
        return float(value)
    except Exception:
        return default
