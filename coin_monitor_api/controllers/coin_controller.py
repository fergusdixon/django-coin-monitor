import os
from datetime import datetime

from django.http import Http404

from coin_monitor_api.clients.coin_gecko_client import CoinGeckoClient
from coin_monitor_api.models import Coin


class CoinController:
    """
    Controller for all things Coin
    """

    # The client
    coin_gecko_client = CoinGeckoClient(api_url=os.getenv('COINGECKO_URL'))

    @classmethod
    def get_coin_list(cls) -> [Coin]:
        """
        Returns a list of coins from the CoinGecko API
        @return: [Coin] The list of coins from CoinGecko
        """
        return cls.coin_gecko_client.get_coin_list()

    @classmethod
    def get_coin_market_cap(cls, coin_id: str, date: datetime, currency) -> float:
        """
        Gets the market cap for a coin ID and currency, on the specified date
        @param coin_id: CoinGecko Coin ID
        @param date: %d-%m-%Y
        @param currency: iso currency symbol
        @return: float
        """
        # Call client
        result = cls.coin_gecko_client.get_coin_history(
            coin_id=coin_id,
            date=date,
            currency=currency
        )

        # Check for errors
        if result.get('errors'):
            return result

        # Get the market cap information
        caps = result.get('market_data', {}).get('market_cap', {})

        # Check the currency exists
        if not caps.get(currency):
            raise Http404()

        return caps.get(currency)
