from __future__ import annotations

import os
from typing import Any


def get_db_config() -> dict[str, Any]:
    password = os.environ.get("INTEREST_DB_PASSWORD", "")
    if not password:
        raise RuntimeError("INTEREST_DB_PASSWORD environment variable is required.")

    return {
        "host": os.environ.get("INTEREST_DB_HOST", "localhost"),
        "port": int(os.environ.get("INTEREST_DB_PORT", "5433")),
        "dbname": os.environ.get("INTEREST_DB_NAME", "portfolio"),
        "user": os.environ.get("INTEREST_DB_USER", "postgres"),
        "password": password,
        "options": "-c search_path=research,decision,execution,connector,preprocessor,interest,reference,legacy,public",
    }
