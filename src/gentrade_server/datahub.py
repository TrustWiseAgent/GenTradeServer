
"""
Data Hub
"""
import os
import logging

from gentrade.market_data.crypto import BinanceMarket
from gentrade.market_data.stock_us import StockUSMarket

LOG = logging.getLogger(__name__)
CURR = os.path.dirname(__file__)

class DataHub:
    """
    Data Hub Class
    """

    _inst = None

    def __init__(self):
        self._markets = {}

    def init(self) -> None:
        """ init """
        cache_dir = os.getenv("GENTRADE_CACHE_DIR",
                              os.path.join(os.path.dirname(__file__), "../../cache/"))
        LOG.info("Cache Directory: %s", cache_dir)
        market_inst = BinanceMarket(cache_dir)
        self._markets[market_inst.market_id] = market_inst
        market_inst = StockUSMarket(cache_dir)
        self._markets[market_inst.market_id] = market_inst
        for market in self._markets.values():
            if not market.init():
                LOG.error("Fail to initialize the market %s", market.name)

    @property
    def markets(self):
        """ property: markets """
        return self._markets

    @staticmethod
    def inst():
        """ Singleton  """
        if DataHub._inst is None:
            DataHub._inst = DataHub()
        return DataHub._inst

    def get_asset(self, asset_name):
        """Get asset from it name

        Args:
            asset_name (_type_): _description_
        """
        for market in self._markets.values():
            if asset_name in market.assets:
                return market.assets[asset_name]
        return None
