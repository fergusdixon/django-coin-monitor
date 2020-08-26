import json

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
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
    def get(self, request: Request, format=None) -> Response:
        # TODO this
        params = request.query_params
        return Response(json.dumps(params))
