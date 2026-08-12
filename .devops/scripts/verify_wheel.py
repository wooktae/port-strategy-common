from __future__ import annotations

import argparse
import hashlib
import sys
import tomllib
import zipfile
from pathlib import Path

PACKAGE_DISTRIBUTION_NAME = "port-strategy-common"
PACKAGE_IMPORT_NAME = "port_strategy_common"

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


def load_project_version() -> str:
    repository_root = Path(__file__).resolve().parents[2]
    pyproject_path = repository_root / "pyproject.toml"

    if not pyproject_path.is_file():
        raise FileNotFoundError(f"pyproject.toml not found: {pyproject_path}")

    with pyproject_path.open("rb") as stream:
        pyproject = tomllib.load(stream)

    project = pyproject.get("project")

    if not isinstance(project, dict):
        raise ValueError("[project] section not found in pyproject.toml")

    name = project.get("name")
    version = project.get("version")

    if name != PACKAGE_DISTRIBUTION_NAME:
        raise ValueError(f"Unexpected project name: {name}")

    if not isinstance(version, str) or not version.strip():
        raise ValueError("Project version is missing")

    return version.strip()


def wheel_version(version: str) -> str:
    return version.replace("-", "_").replace("+", "_")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("wheel", type=Path)
    args = parser.parse_args()

    wheel = args.wheel.resolve()

    if not wheel.is_file():
        raise FileNotFoundError(f"Wheel not found: {wheel}")

    project_version = load_project_version()

    expected_wheel_name = (
        f"{PACKAGE_IMPORT_NAME}-"
        f"{wheel_version(project_version)}-"
        "py3-none-any.whl"
    )

    if wheel.name != expected_wheel_name:
        raise ValueError(
            f"Unexpected wheel name: {wheel.name}; "
            f"expected: {expected_wheel_name}"
        )

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

    print(f"PACKAGE_VERSION={project_version}")
    print(f"WHEEL_NAME={wheel.name}")
    print(f"WHEEL_SIZE={wheel.stat().st_size}")
    print(f"WHEEL_SHA256={sha256(wheel)}")
    print(f"WHEEL_MEMBER_COUNT={len(members)}")
    print("COMMON_WHEEL_STRUCTURE=SUCCESS")

    return 0


if __name__ == "__main__":
    sys.exit(main())