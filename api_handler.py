import requests

class ApiHandler:
    """Parse given message and then request to Crypto API.
        Send back response from Crypto API.
    """
    def __init__(self):
        self.api_url = 'https://api.cryptonator.com/api/full/'

    def get_response(self, text):
        """Parse text, and return appropriate response."""
        if '-' in text:
            args = text.split(' ')
            if len(args) > 2:
                return 'Unrecognized command: <{}> Please see /help'.format(text)
            pair = args[0]
            res = self.request_api(pair)
            if res['success'] == True:
                market = args[1] if len(args) == 2 else None
                return self.format_answer(res, market)
                # return self.format_currency(res['ticker']['price'])
            else:
                if res['error'] == 'Pair not found':
                    return 'Pair <{}> not found. Please try another pair'.format(text)
                else:
                    return 'Sorry, request failed. Please try again later.'
        else:
            return 'Unrecognized command: <{}> Please try again'.format(text)

    def request_api(self, req):
        """Send request to api url, then return response in json."""
        res = requests.get(self.api_url + req)
        print("getting response from crypto api...")
        return res.json()

    def format_currency(self, amount, offset=False):
        """"Return string of amount in currency format"""
        return '{:20,}'.format(float(amount))

    def format_answer(self, res, market=None):
        """Accept json from crypto API's response. Format answer and return as string."""
        available = "No specific market is available.\n"
        price = self.format_currency(res['ticker']['price'])
        vol = self.format_currency(res['ticker']['volume'])
        if len(res['ticker']['markets']) > 0 and market:
            for obj in res['ticker']['markets']:
                if obj['market'].lower() == market.lower():
                    price = self.format_currency(obj['price'])
                    vol = self.format_currency(obj['volume'])
                    available = "Price of {base} in {market} Market\n".format(base=res['ticker']['base'], market=market)
            
        answer = """{available}
            Price : {price}\n
            Volume : {volume}\n
            """.format(available=available, price=price, volume=vol)

        return answer
