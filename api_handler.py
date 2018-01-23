import requests

class ApiHandler:
    """parse given message and then request to Crypto API.
        Send back response from Crypto API.
    """
    def __init__(self):
        self.api_url = 'https://api.cryptonator.com/api/full/'

    def get_response(self, text):
        """parse text, and return appropriate response."""
        if '-' in text:
            res = self.request_api(text)
            if res['success'] == True:
                return res['ticker']['price']
            else:
                return 'Sorry, request failed. Please try again later.'
        else:
            return 'Unrecognized command: <{}> Please try again'.format(text)

    def request_api(self, req):
        """Send request to api url, then return response in json."""
        res = requests.get(self.api_url + req)
        print("getting response from crypto api...")
        return res.json()
