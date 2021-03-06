import json

from django.test import Client, TestCase


class CoinListTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_coin_list(self):
        """
        Given: the client
        When: The '/coinList' url is called
        Then: A list of CoinGecko coins is returned
        @return:
        """
        response = self.client.get('/coinList/')
        coins = json.loads(response.content)

        self.assertGreater(len(coins), 0)
        self.assertTrue(coins[0].get('id'))
        self.assertTrue(coins[0].get('name'))
        self.assertTrue(coins[0].get('symbol'))


class MarketCapTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_valid_market_cap(self):
        """
        Given: A client
        When: Calling the '/marketCap' endpoint with a valid coin_id
        Then: the market cap for the specified currency is returned
        @return:
        """
        # get a valid coin_id
        response = self.client.get('/coinList/')
        coins = json.loads(response.content)
        self.assertGreater(len(coins), 0)

        params = {
            'coin_id': coins[0].get('id'),
            'date': '2020/08/05',
            'currency': 'gbp'
        }
        response = self.client.get('/marketCap/', data=params)

        market_cap = json.loads(response.content)

        self.assertGreater(len(market_cap), 0)
        self.assertTrue(market_cap.get('gbp', False))
        self.assertEqual(type(market_cap.get('gbp')), float)

    def test_get_market_cap_malformed_date(self):
        """
        Given: A client
        When: Calling the '/marketCap' endpoint with a malformed date
        Then: and error is returned
        @return:
        """
        # get a valid coin_id
        response = self.client.get('/coinList/')
        coins = json.loads(response.content)
        self.assertGreater(len(coins), 0)

        params = {
            'coin_id': coins[0].get('id'),
            'date': '2020-08-05',
            'currency': 'gbp'
        }
        response = self.client.get('/marketCap/', data=params)

        json_result = json.loads(response.content)
        self.assertEqual(400, response.status_code)
        self.assertGreater(len(json_result), 0)
        self.assertEqual(json_result[0], 'date should be in the YYYY/MM/DD format')
