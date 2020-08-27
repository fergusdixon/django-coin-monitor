import os
from datetime import datetime

from django.http import Http404

from coin_monitor_api.clients.coin_gecko_client import CoinGeckoClient
from coin_monitor_api.models import Coin


class CoinController:
    coin_gecko_client = CoinGeckoClient(api_url=os.getenv('COINGECKO_URL'))

    @classmethod
    def get_coin_list(cls) -> [Coin]:
        return cls.coin_gecko_client.get_coin_list()

    @classmethod
    def get_coin_market_cap(cls, coin_id: str, date: datetime, currency) -> {}:
        result = cls.coin_gecko_client.get_coin_history(
            coin_id=coin_id,
            date=date,
            currency=currency
        )
        if result.get('errors'):
            return result
        caps = result.get('market_data', {}).get('market_cap', {})
        if not caps.get(currency):
            raise Http404()
        return caps.get(currency)
