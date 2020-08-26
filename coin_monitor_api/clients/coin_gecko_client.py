"""
Simple client for https://www.coingecko.com/en/api

Could have used this client: https://github.com/man-c/pycoingecko
"""
from datetime import datetime
from typing import List

import requests
from pydantic import parse_obj_as
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from coin_monitor_api.models import Coin


class CoinGeckoClient:
    def __init__(self, api_url):
        self.api_url = api_url
        self.timeout = 10
        retries = Retry(total=3, backoff_factor=0.2, status_forcelist=[502, 503, 504])
        self.session = requests.Session()
        self.session.mount('https://', HTTPAdapter(max_retries=retries))

    def get_coin_list(self) -> [Coin]:
        endpoint = 'coins/list'
        request_url = f'{self.api_url}{endpoint}'
        response = self.session.get(request_url, timeout=self.timeout)
        coins = parse_obj_as(List[Coin], response.json())
        return coins

    def get_coin_history(self, coin_id, date: datetime, currency: str) -> {}:
        endpoint = f'coins/{coin_id}/history'
        request_url = f'{self.api_url}{endpoint}'
        params = {
            'vs_currency': currency,
            'date': date.strftime('%d-%m-%Y'),
            'localization': 'false'
        }

        response = self.session.get(request_url, params=params, timeout=self.timeout)
        return response.json()
