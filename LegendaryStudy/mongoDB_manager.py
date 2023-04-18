import datetime
from pymongo import MongoClient
import os


class mongo_manager:

    client=None

    def __init__(self,user=None,pssw=None):
        if user is None and pssw is None:
            user = os.getenv('MONGO_USER')
            pssw = os.getenv('MONGO_PSSW')

        conn = "mongodb+srv://"+user+":"+pssw+"@legendarystudy.c4uj7ri.mongodb.net/?retryWrites=true&w=majority"
        if self.client is None:
            self.client = MongoClient(conn)


    def __get_coll__(self):
        if self.client is not None:
            mydb = self.client["db"]
            mycol = mydb["user_data"]
            return mycol


    def load_backup(self, backup):
        self.__get_coll__().insert_one({"date_insert":str(datetime.datetime.now()),"backup":backup})
        return {"success": True}

    def get_users_files(self):
        return self.__get_coll__().find()

