import unittest
from importlib.metadata import distribution
from pathlib import Path

import port_strategy_common
import tomllib
from port_strategy_common.common_buy_decision import CommonBuyDecision
from port_strategy_common.common_context import (
    CommonPositionContext,
    CommonStockContext,
)
from port_strategy_common.common_sell_decision import CommonSellDecision
from port_strategy_common.common_types import (
    CommonMarketSignal,
    CommonTradeSignal,
)
from port_strategy_common.common_version import COMMON_STRATEGY_VERSION


def load_project_version() -> str:
    repository_root = Path(__file__).resolve().parents[1]
    pyproject_path = repository_root / "pyproject.toml"

    with pyproject_path.open("rb") as stream:
        pyproject = tomllib.load(stream)

    project = pyproject["project"]

    version = project["version"]

    if not isinstance(version, str) or not version.strip():
        raise ValueError("Project version is missing")

    return version.strip()


class PublicContractTest(unittest.TestCase):
    def test_distribution_metadata(self) -> None:
        installed = distribution("port-strategy-common")
        expected_version = load_project_version()

        self.assertEqual(
            installed.metadata["Name"],
            "port-strategy-common",
        )
        self.assertEqual(
            installed.version,
            expected_version,
        )

    def test_strategy_version(self) -> None:
        self.assertEqual(
            COMMON_STRATEGY_VERSION,
            "COMMON_STRATEGY_V1.0.0",
        )

    def test_public_symbols_are_importable(self) -> None:
        symbols = [
            CommonPositionContext,
            CommonStockContext,
            CommonBuyDecision,
            CommonSellDecision,
            CommonMarketSignal,
            CommonTradeSignal,
        ]

        self.assertEqual(len(symbols), 6)

        for symbol in symbols:
            self.assertTrue(callable(symbol))

    def test_package_is_installed(self) -> None:
        package_file = str(port_strategy_common.__file__)

        self.assertIn(
            "site-packages",
            package_file.lower(),
        )
        self.assertNotIn(
            r"c:\workspaces\port_strategy_common",
            package_file.lower(),
        )


if __name__ == "__main__":
    unittest.main()