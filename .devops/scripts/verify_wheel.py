from __future__ import annotations

import argparse
import hashlib
import sys
import zipfile
from pathlib import Path

REQUIRED_PACKAGE_FILES = {
    "port_strategy_common/__init__.py",
    "port_strategy_common/common_context.py",
    "port_strategy_common/common_buy_decision.py",
    "port_strategy_common/common_sell_decision.py",
    "port_strategy_common/common_types.py",
    "port_strategy_common/common_version.py",
}

FORBIDDEN_PARTS = {
    "__pycache__",
    ".pyc",
    ".git",
    "docs",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("wheel", type=Path)
    args = parser.parse_args()

    wheel = args.wheel.resolve()

    if not wheel.is_file():
        raise FileNotFoundError(f"Wheel not found: {wheel}")

    if wheel.name != "port_strategy_common-1.0.0rc1-py3-none-any.whl":
        raise ValueError(f"Unexpected wheel name: {wheel.name}")

    with zipfile.ZipFile(wheel) as archive:
        members = set(archive.namelist())

    missing = sorted(REQUIRED_PACKAGE_FILES - members)

    if missing:
        raise ValueError(
            "Required package files are missing: "
            + ", ".join(missing)
        )

    forbidden = sorted(
        member
        for member in members
        if any(
            part == forbidden
            or part.endswith(forbidden)
            for part in Path(member).parts
            for forbidden in FORBIDDEN_PARTS
        )
    )

    if forbidden:
        raise ValueError(
            "Forbidden wheel entries found: "
            + ", ".join(forbidden)
        )

    print(f"WHEEL_NAME={wheel.name}")
    print(f"WHEEL_SIZE={wheel.stat().st_size}")
    print(f"WHEEL_SHA256={sha256(wheel)}")
    print(f"WHEEL_MEMBER_COUNT={len(members)}")
    print("COMMON_WHEEL_STRUCTURE=SUCCESS")

    return 0


if __name__ == "__main__":
    sys.exit(main())