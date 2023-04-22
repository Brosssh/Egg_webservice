import datetime
from datetime import timedelta
from pymongo import MongoClient
import os


class mongo_manager:

    client=None

    def __init__(self,user=None,pssw=None,host=None):
        user_final=user if user is not None else os.getenv('MONGO_USER')
        pssw_final=pssw if pssw is not None else os.getenv('MONGO_PSSW')
        host_final=host if host is not None else "legendarystudy.c4uj7ri.mongodb.net"
        conn = "mongodb+srv://"+user_final+":"+pssw_final+"@"+host_final+"/?retryWrites=true&w=majority"
        if self.client is None:
            self.client = MongoClient(conn, connect=False)


    def __get_coll__(self):
        if self.client is not None:
            mydb = self.client["db"]
            mycol = mydb["user_data"]
            return mycol

    def __get_reports_coll__(self):
        if self.client is not None:
            mydb = self.client["reports"]
            mycol = mydb["legendaryStudyReports"]
            return mycol


    def load_backup(self, backup):
        old_doc=self.__get_coll__().find_one({"backup.eiUserId":backup["eiUserId"]})
        if old_doc is not None:
            self.__get_coll__().delete_one({"backup.eiUserId":backup["eiUserId"]})
        self.__get_coll__().insert_one({"date_insert":str(datetime.datetime.now()),"backup":backup})
        return {"success": True}

    def get_users_files(self):
        return self.__get_coll__().find()

    def load_daily_report_legendary(self, file):
        old_doc = self.__get_reports_coll__().find_one({"date_insert":str(datetime.date.today())})
        if old_doc is not None:
            self.__get_reports_coll__().delete_one({"date_insert":str(datetime.date.today())})
        self.__get_reports_coll__().insert_one({"date_insert":str(datetime.date.today()),"report":file})
        return {"success": True}


    def get_last_report_legendary(self):
        return self.__get_reports_coll__().find().sort("date_insert",-1)[0]

    def get_report_by_date(self,date):
        return self.__get_reports_coll__().find({"date_insert":date})
