import datetime
from pymongo import MongoClient



class mongo_manager:

    client=None

    def __init__(self,conn_string):
        if self.client is None:
            self.client = MongoClient(conn_string)


    def __get_coll__(self):
        if self.client is not None:
            mydb = self.client["db"]
            mycol = mydb["user_data"]
            return mycol


    def load_backup(self, backup):
        self.__get_coll__().insert_one({"date_insert":str(datetime.datetime.now()),"backup":backup})
        return {"success": True}

