import json

from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from coin_monitor_api.controllers.coin_controller import CoinController


@api_view(['GET'])
def get_coin_list(request: Request) -> Response:
    coins = CoinController().get_coin_list()
    # TODO look at cleaning this up
    return Response([coin.dict() for coin in coins])


@api_view(['GET'])
def get_market_cap(request: Request) -> Response:
    # TODO query param validation
    params = request.query_params
    return Response(json.dumps(params))
