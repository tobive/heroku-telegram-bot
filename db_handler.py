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
    """
    def __init__(self):
        client = MongoClient(port=27017)
        if client:
            self.db = client.crypto_price
        else:
            self.db = None

    def save_alarm(self, pairing, market, direction, price):
        fail_msg = "Failed to create alarm. Please try again later"
        if(self.db):
            alarm = {
                "pairing" : pairing,
                "market" : market,
                "direction" : direction,
                "price" : price,
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
        # delete record with delete_id
        result = self.db.alarms.delete_one({"delete_id": delete_id})
        # check result
        if result.deleted_count:
            return "Successfully deleted alarm"
        else:
            return "Error. Failed to delete alarm"
