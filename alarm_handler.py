from api_handler import ApiHandler
from db_handler import DbHandler
from time import sleep

class AlarmHandler:
    def __init__(self, TOKEN):
        self.db_handler = DbHandler()
        self.api_handler = ApiHandler()
        self.TOKEN = TOKEN

    def run_manager(self):
        """Do all operations."""
        # Check all registered pairing-market in alarms Collection
        list_alarm = self.db_handler.get_list_alarm_pairing()
        list_pairing = self.db_handler.get_list_pairing_only()
        # Use API handler to fetch new price from list of pairing only
        # This way, request to API only based on list of pairing
        list_new_price = []
        for pair in list_pairing:
            json = self.api_handler.request_api(pair)
            # Update list_new_price with pairing-market price from API data
            for alarm in list_alarm:
                if alarm["pairing"] == pair:
                    list_new_price.append(self.fetch_price_market(alarm, json))
            sleep(0.1)
        # Update/Add price in market_prices Collection
        for price in list_new_price:
            self.db_handler.save_market_price(**price)
        # Check for triggered alarm
        list_alarm = self.db_handler.get_alarms()
        list_price = self.db_handler.get_list_market_price()
        list_triggered_id = self.check_triggered_alarm(list_alarm, list_price)
        for id in list_triggered_id:
            for alarm in list_alarm:
                if id == alarm["_id"]:
                    # Notify user based on chat_id
                    self.api_handler.notify_alarm(alarm, self.TOKEN)
                    print("notify chat_id : {}".format(alarm["chat_id"]))
                    # Delete triggered alarm, delete pairing-market in market_prices Collection
                    self.db_handler.delete_alarm(alarm["delete_id"])
                    self.db_handler.delete_market_price(alarm["pairing"], alarm["market"])

    def fetch_price_market(self, pair_obj, res_json):
        """Took json response from API handler, return price in ready to be saved dictionary."""
        result = {
            "pairing" : pair_obj["pairing"],
            "market" : pair_obj["market"],
            "time" : res_json["timestamp"],
            "price" : 0
        }
        # If market found, assign the market price, else assign general market
        for market in res_json["ticker"]["markets"]:
            if market["market"].lower() == pair_obj["market"].lower():
                result["price"] = market["price"]
        if result["price"]:
            return result
        else:
            result["price"] = res_json["ticker"]["price"]
            return result

    def check_triggered_alarm(self, list_alarm, list_price):
        """Returns list of id of triggered alarm."""
        # list_alarm = self.db_handler.get_list_alarm_pairing()
        # list_price = self.db_handler.get_list_market_price()

        res = []
        for alarm in list_alarm:
            for price in list_price:
                if alarm["pairing"] == price["pairing"] and alarm["market"] == price["market"]:
                    if alarm["direction"] == 'above' and float(alarm["price"]) <= float(price["price"]):
                         res.append(alarm["_id"])
                    if alarm["direction"] == 'below' and float(alarm["price"]) >= float(price["price"]):
                         res.append(alarm["_id"])
        return res

    def echo_dummy(self):
        print("###### ------- echo dummy ------ ######")
