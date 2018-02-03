from pymongo import MongoClient, ReturnDocument
import hashlib

class DbHandler:
    """Connect to Mongo DB and handles the CRUD operations on database.
    Database scheme:
        alarms : {
            _id : Mongo Obj ID,
            chat_id : string,
            pairing : string,
            market : string,
            direction: string,
            price : float,
            delete_id : hash
        }

        market_prices : {
            _id : Mongo Obj ID,
            pairing : string,
            market : string,
            price : string,
            time : time
        }
    """
    def __init__(self):
        client = MongoClient(port=27017)
        if client:
            self.db = client.crypto_price
        else:
            self.db = None

    def save_alarm(self, pairing, market, direction, price, chat_id):
        """Save alarm."""
        fail_msg = "Failed to create alarm. Please try again later"
        if(self.db):
            alarm = {
                "pairing" : pairing.lower(),
                "market" : market.lower(),
                "direction" : direction.lower(),
                "price" : price,
                "chat_id" : chat_id,
                "delete_id" : 0
            }
            # save to collection
            alarm_id = self.db.alarms.insert_one(alarm)
            alarm_id_str = str(alarm_id.inserted_id)
            # check if insert success
            if alarm_id:
                # hash the returned alarm id in string format
                del_id = hashlib.md5(alarm_id_str.encode())
                # update record with delete_id from hash
                new_alarm = self.db.alarms.find_one_and_update(
                    {'_id' : alarm_id.inserted_id},
                    {'$set' : {'delete_id' : del_id.hexdigest()}},
                    return_document=ReturnDocument.AFTER)
                # return result
                if new_alarm:
                    return "Successfully created alarm"
                else:
                    return fail_msg
            else:
                return fail_msg
        else:
            return fail_msg

    def delete_alarm(self, delete_id):
        """Delete alarm based on delete_id."""
        # delete record with delete_id
        result = self.db.alarms.delete_one({"delete_id": delete_id})
        # check result
        if result.deleted_count:
            return "Successfully deleted alarm"
        else:
            return "Error. Failed to delete alarm"

    def save_market_price(self, pairing, market, price, time):
        """Save or update current market price."""
        fail_msg = "Failed to create alarm. Please try again later"
        if(self.db):
            market_price = {
                "pairing" : pairing.lower(),
                "market" : market.lower(),
                "price" : price,
                "time" : time
            }
            # save to collection, update if already exist
            mp_id = self.db.market_prices.update_one(
                {"pairing" : pairing.lower(), "market": market.lower()},
                {"$set": market_price},
                upsert=True)
            # check if insert success
            if mp_id:
                return "success."
            else:
                return fail_msg
        else:
            return fail_msg

    def delete_market_price(self, pairing, market):
        """Delete market price based on pairing and/or market."""
        # delete record with delete_id
        result = self.db.market_prices.delete_one(
            {   "pairing" : pairing.lower(),
                "market" : market.lower()
            })
        # check result
        if result.deleted_count:
            return "Successfully deleted alarm"
        else:
            return "Error. Failed to delete alarm"

    def get_list_alarm_pairing(self):
        """Return a list of all registered pairing and market in db."""
        list_pairing = self.db.alarms.find(
            {},
            { "pairing":1, "market":1, "direction":1, "price":1, "_id":1 })
        res = []
        # removes duplicates
        for doc in list_pairing:
            if doc not in res:
                res.append(doc)
        return res

    def get_list_pairing_only(self):
        """Return a list of all registered pairing only."""
        list_pairing = self.db.alarms.distinct('pairing')
        return list_pairing

    def get_alarms(self):
        list_alarms = self.db.alarms.find({})
        res = []
        for alarm in list_alarms:
            res.append(alarm)
        return res

    def get_list_market_price(self):
        """Return list of market price."""
        list_price = self.db.market_prices.find({})
        res = []
        for price in list_price:
            res.append(price)
        return res
