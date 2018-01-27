import unittest
from api_handler import ApiHandler
import responses

class TestApiHandler(unittest.TestCase):

    def setUp(self):
        self.bot = ApiHandler()
        self.req = "xlm-idr"
        # Mock response from crypto API server
        responses.add(**{
            'method' : responses.GET,
            'url' : self.bot.api_url,
            'body' : {
                "ticker":
                    {   "base":"XLM",
                        "target":"IDR",
                        "price":"7513.33375000",
                        "volume":"",
                        "change":"179.43967000",
                        "markets":[]
                    },
                "timestamp":1516788422,
                "success":True,
                "error":""
                },
            'status' : 200,
            'content_type' : 'application/json'
        })

    def test_get_response(self):
        text = "xlm-idr"
        self.assertEqual(self.bot.get_response(text), self.bot.format_answer(self.bot.request_api(text)))
        text = "xlm-idr bitfinex ok"
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



if __name__ == '__main__':
    unittest.main()
