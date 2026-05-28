"""DB 접속 설정을 환경변수에서 로드하는 helper 모듈.

`INTEREST_DB_*` 값을 읽어 connection config dictionary를 반환한다.
비밀번호 기본값은 제공하지 않으며, 실제 DB 연결이나 DDL/DML 실행은 수행하지 않는다.
"""

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
