from LegendaryStudy import auxbrain_manager
from LegendaryStudy.utility import encrypt_string, protoToJson, protoToDict


def submitEID(mongo, EID):
    try:
        auxbrain=auxbrain_manager.auxbrain(EID)
        response_auxbrain=auxbrain.get_bot_first_contact()

        if response_auxbrain["success"] and response_auxbrain["response"] is not None:
            backup = response_auxbrain["response"].backup
            backup.ei_user_id = encrypt_string(EID)
            backup_dict=protoToDict(backup)

            #remove stuff too big to save space
            shipsCountArchiveAR={}
            for el in backup_dict["artifactsDb"]['missionArchive']:
                if el["ship"] not in shipsCountArchiveAR:
                    shipsCountArchiveAR[el["ship"]+":"+el["durationType"]]=1
                else:
                    shipsCountArchiveAR[el["ship"]+":"+el["durationType"]]+=1
            backup_dict["artifactsDb"]['shipsCountArchiveAR']=shipsCountArchiveAR

            del backup_dict["artifactsDb"]['missionArchive']
            del backup_dict["contracts"]
            del backup_dict["tutorial"]
            del backup_dict["game"]["news"]
            del backup_dict["game"]["achievements"]
            del backup_dict["mission"]
            del backup_dict["farms"]



            result=mongo.load_backup(backup_dict)
            if result["success"]:
                return {"success":True,"message":"OK"}
            else:
                return {"success": False, "message": "Error loading backup in Mongo"}
        return {"success": False, "message": "Backup empty"}
    except Exception as e:
        return {"success": False, "message": str(e)}


def getReport(mongo, date):
    return mongo.get_report_by_date(date)