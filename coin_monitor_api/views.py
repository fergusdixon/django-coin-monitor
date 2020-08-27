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
        coin_id = request.query_params.get('coin_id')
        if not coin_id:
            raise ValidationError('coin_id is required')

        try:
            date = request.query_params.get('date')
            if not date:
                raise ValidationError('date is required')
            date = datetime.strptime(date, '%Y/%m/%d')
        except ValueError:
            raise ValidationError('date should be in the YYYY/MM/DD format')

        currency = request.query_params.get('currency')
        if not currency:
            raise ValidationError('currency is required')

        market_cap = CoinController.get_coin_market_cap(coin_id=coin_id, date=date, currency=currency)
        return Response({currency: market_cap})
