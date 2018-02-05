import unittest
from api_handler import ApiHandler
import responses

class TestApiHandler(unittest.TestCase):

    def setUp(self):
        self.bot = ApiHandler()
        self.req = "btc-usd"
        # Mock response from crypto API server
        responses.add(**{
            'method' : responses.GET,
            'url' : self.bot.api_url,
            'body': {
                "ticker": {
                    "base":"BTC",
                    "target":"USD",
                    "price":"11162.55588755",
                    "volume":"100552.47050345",
                    "change":"-6.09952832",
                    "markets":[
                        {"market":"BitFinex","price":"11129.00000000","volume":54929.67631363},
                        {"market":"Bitstamp","price":"11154.47000000","volume":14375.43966681},
                        {"market":"Bittrex","price":"11110.00000000","volume":6567.83057287},
                        {"market":"C-Cex","price":"12130.00000000","volume":3.70034411},
                        {"market":"Cex.io","price":"11854.90000000","volume":1656.26180368},
                        {"market":"Exmo","price":"11966.03000000","volume":1315.8619739},
                        {"market":"Hitbtc","price":"11116.62000000","volume":6478.02},
                        {"market":"Kraken","price":"11129.60000000","volume":7572.35982247},
                        {"market":"Livecoin","price":"11740.41021000","volume":910.06289355},
                        {"market":"Poloniex","price":"11130.00000013","volume":6072.57512243},
                        {"market":"wexnz","price":"11633.76000000","volume":670.68199}
                        ]
                    },
                "timestamp":1517027522,
                "success":True,
                "error":""
            },
            'status' : 200,
            'content_type' : 'application/json'
        })

    def test_get_response(self):
        text = "btc-usd"
        self.assertEqual(self.bot.get_response(text), self.bot.format_answer(self.bot.request_api(text)))
        text = "btc-usd bitfinex ok"
        self.assertEqual(self.bot.get_response(text), 'Unrecognized command: <{}> Please see /help'.format(text))

    def test_request_api(self):
        self.assertTrue(isinstance(self.bot.request_api(self.req), dict))

    def test_format_currency(self):
        amount = None
        self.assertEqual(self.bot.format_currency(8000000), "8,000,000.0")
        self.assertEqual(self.bot.format_currency("8000000"), "8,000,000.0")
        self.assertEqual(self.bot.format_currency(0.00004600), "0.00004600")
        self.assertEqual(self.bot.format_currency("0.00004600"), "0.00004600")
        self.assertEqual(self.bot.format_currency("4.6e-5"), "0.00004600")
        self.assertEqual(self.bot.format_currency(amount), "not available")
        self.assertEqual(self.bot.format_currency(""), "not available")
        self.assertEqual(self.bot.format_currency([]), "not available")

    def test_format_answer(self):
        pass

    def test_list_markets(self):
        obj = {
            "ticker" : {
                "markets" : [
                    {
                        "market" : "BitFinex"
                    },
                    {
                        "market" : "Kraken"
                    }
                ]
            }
        }
        self.assertEqual(self.bot.list_markets(obj), "BitFinex, Kraken")

    def test_is_market_available(self):
        res = self.bot.request_api("btc-usd")
        self.assertEqual(self.bot.is_market_available(res, "Kraken"), True)
        self.assertEqual(self.bot.is_market_available(res, "Kleleken"), False)


if __name__ == '__main__':
    unittest.main()
