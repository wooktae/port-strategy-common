import unittest
from importlib.metadata import distribution

import port_strategy_common
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


class PublicContractTest(unittest.TestCase):
    def test_distribution_metadata(self) -> None:
        installed = distribution("port-strategy-common")

        self.assertEqual(installed.metadata["Name"], "port-strategy-common")
        self.assertEqual(installed.version, "1.0.0rc1")

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

        self.assertIn("site-packages", package_file.lower())
        self.assertNotIn(
            r"c:\workspaces\port_strategy_common",
            package_file.lower(),
        )


if __name__ == "__main__":
    unittest.main()