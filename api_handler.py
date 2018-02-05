import requests

class ApiHandler:
    """Handles all things related to Crypto API.
    """
    def __init__(self):
        self.api_url = 'https://api.cryptonator.com/api/full/'

    def get_response(self, text):
        """Parse text, and return appropriate response."""
        if '-' in text:
            args = text.split(' ')
            if len(args) > 2:
                return 'Unrecognized command: <{}> Please see /help'.format(text)
            if args[0] == 'market':
                pair = args[1]
                res = self.request_api(pair)
                return self.list_markets(res)
            pair = args[0]
            res = self.request_api(pair)
            if res['success'] == True:
                market = args[1] if len(args) == 2 else None
                return self.format_answer(res, market)
            else:
                if res['error'] == 'Pair not found':
                    return 'Pair <{}> not found. Please try another pair'.format(text)
                else:
                    return 'Sorry, request failed. Please try again later.'
        else:
            return 'Unrecognized command: <{}> Please see /help'.format(text)

    def request_api(self, pair):
        """Send request to api url, then return response in json."""
        res = requests.get(self.api_url + pair)
        print("getting response from crypto api...")
        # print(res.json())
        return res.json()

    def format_currency(self, amount, offset=False):
        """"Return string of amount in currency format"""
        amount = amount if amount else 0
        sum = float(amount)
        if sum > 1:
            return '{:20,}'.format(sum).replace(" ", "")
        elif sum < 1 and sum > 0: # satoshis
            return format(sum, '.8f')
        else:
            return 'not available'

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
            ```\nPrice ({target}) : {price}\nVolume      : {volume}```\n
            """.format(available=available, target=res['ticker']['target'], price=price, volume=vol)
        return answer

    def list_markets(self, res):
        """Returns string of available markets from response"""
        if res['ticker']['markets'] == []:
            return 'Sorry, no specific market is available'
        the_list = []
        for market in res['ticker']['markets']:
            the_list.append(market['market'])
        return ", ".join(the_list)

    def is_market_available(self, res, market):
        """Return boolean of whether a market is available on certain pairing."""
        for target in res['ticker']['markets']:
            if market.lower() == target["market"].lower():
                return True
        return False

    def notify_alarm(self, alarm_obj, TOKEN):
        """Send to telegram api to notify the triggered alarm based on chat_id."""
        telegram_url = "https://api.telegram.org/bot{token}/sendMessage?parse_mode=Markdown&chat_id={chat_id}&text=".format(
            token=TOKEN,
            chat_id=alarm_obj["chat_id"]
        )
        msg_string = """* **ALARM TRIGGERED** *\n_Pair_ : {pair}\n_Market_ : {market}\n_Direction_ : {direction}\n_Price_ : {price}""".format(
            pair=alarm_obj["pairing"],
            market=alarm_obj["market"],
            direction=alarm_obj["direction"],
            price=alarm_obj["price"]
        )
        res = requests.get(telegram_url + msg_string)
