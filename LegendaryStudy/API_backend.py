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
            #backup_dict.pop('key', None)
            result=mongo.load_backup(backup_dict)
            if result["success"]:
                return {"success":True,"message":"OK"}
            else:
                return {"success": False, "message": "Error loading backup in Mongo"}
        return {"success": False, "message": "Backup empty"}
    except Exception as e:
        return {"success": False, "message": str(e)}