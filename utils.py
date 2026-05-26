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
