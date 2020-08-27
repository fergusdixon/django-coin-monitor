from datetime import datetime

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from coin_monitor_api.controllers.coin_controller import CoinController


class CoinList(APIView):
    @method_decorator(cache_page(60 * 60))
    def get(self, request: Request, format=None) -> Response:
        coins = CoinController().get_coin_list()
        # TODO look at cleaning this up
        return Response([coin.dict() for coin in coins])


class MarketCapDetail(APIView):
    @method_decorator(cache_page(60 * 60))
    def get(self, request: Request, format=None) -> Response:
        """
        Returns the market cap for a coin ID and currency, on a specific data
        @param request: params:
        coin_id: required
        date: required - %Y/%m/%d
        currency: required
        @param format:
        @return: Response:
        {
            "gbp": 10294177055.519627
        }
        """

        # Get validate parameters
        coin_id, date, currency = self._validate_get_params(request)

        # Get the market cap
        market_cap = CoinController.get_coin_market_cap(coin_id=coin_id, date=date, currency=currency)

        return Response({currency: market_cap})

    @staticmethod
    def _validate_get_params(request: Request) -> (str, datetime, str):
        coin_id = request.query_params.get('coin_id')

        # Validate coin_id
        if not coin_id:
            raise ValidationError('coin_id is required')

        # Validate date
        try:
            date = request.query_params.get('date')
            if not date:
                raise ValidationError('date is required')
            date = datetime.strptime(date, '%Y/%m/%d')
        except ValueError:
            raise ValidationError('date should be in the YYYY/MM/DD format')

        # Validate currency
        currency = request.query_params.get('currency')
        if not currency:
            raise ValidationError('currency is required')

        return coin_id, date, currency
