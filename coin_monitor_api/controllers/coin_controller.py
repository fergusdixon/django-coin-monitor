import os

from coin_monitor_api.clients.coin_gecko_client import CoinGeckoClient
from coin_monitor_api.models import Coin


class CoinController:
    coin_gecko_client = CoinGeckoClient(api_url=os.getenv('COINGECKO_URL'))

    @classmethod
    def get_coin_list(cls) -> [Coin]:
        return cls.coin_gecko_client.get_coin_list()
