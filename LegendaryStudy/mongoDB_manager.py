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
        old_doc = self.__get_reports_coll__().find_one({"date_insert":int(datetime.datetime.utcnow().timestamp())})
        if old_doc is not None:
            self.__get_reports_coll__().delete_one({"date_insert":int(datetime.datetime.utcnow().timestamp())})
        self.__get_reports_coll__().insert_one({"date_insert":int(datetime.datetime.utcnow().timestamp()),"report":file})
        return {"success": True}


    def get_last_report_legendary(self):
        return self.__get_reports_coll__().find().sort("date_insert",-1)[0]

    def get_anonymus_legendary_report_by_date(self,date):
        file=self.__get_reports_coll__().find_one({"date_insert":date})
        if file is None:
            return None
        else:
            del file["_id"]
            leg_seen_list=file["report"]["leg_seen"]
            for el in leg_seen_list:
                file["report"]["leg_seen"][el]=len(file["report"]["leg_seen"][el])
            legendary_players_list = file["report"]["legendary_players"]
            for el in legendary_players_list:
                file["report"]["legendary_players"][el]=len(file["report"]["legendary_players"][el])
            #sort
            file["report"]["legendary_players"]={str(key):file["report"]["legendary_players"][str(key)] for key in sorted([int(el) for el in file["report"]["legendary_players"].keys()],reverse=True)}
            file["report"]["leg_seen"]={r: file["report"]["leg_seen"][r] for r in sorted(file["report"]["leg_seen"], key=file["report"]["leg_seen"].get, reverse=True)}
            return file

    def get_timestamps_legendary_report(self):
        return [el["date_insert"] for el in list(self.__get_reports_coll__().find({},{"date_insert":1,"_id":0}).sort("date_insert",-1))]
