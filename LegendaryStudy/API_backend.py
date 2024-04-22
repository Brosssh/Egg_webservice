from collections import Counter

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
                if el["ship"]+":"+el["durationType"] not in shipsCountArchiveAR:
                    shipsCountArchiveAR[el["ship"]+":"+el["durationType"]]=1
                else:
                    shipsCountArchiveAR[el["ship"]+":"+el["durationType"]]+=1
            backup_dict["artifactsDb"]['shipsCountArchiveAR']=shipsCountArchiveAR

            try:
                total_crafts = backup_dict["artifactsDb"]["artifactStatus"]
                expected_drop_l = int(shipsCountArchiveAR["HENERPRISE:EPIC"] if "HENERPRISE:EPIC"in shipsCountArchiveAR.keys() else 0) / 25 \
                                  + int(shipsCountArchiveAR["HENERPRISE:LONG"] if "HENERPRISE:LONG"in shipsCountArchiveAR.keys() else 0) / (4.5 * 25) \
                                  + int(shipsCountArchiveAR["HENERPRISE:SHORT"] if "HENERPRISE:SHORT"in shipsCountArchiveAR.keys() else 0) / (6 * 25)
                expected_craft_l = sum(el["count"] for el in total_crafts if ("GREATER" in str(el["spec"]) and "LUNAR_TOTEM" not in str(el["spec"])) or ("TUNGSTEN_ANKH" in str(el["spec"]) and "NORMAL" in str(el["spec"]))) * 0.0085

                inventory_items = backup_dict["artifactsDb"]["inventoryItems"]

                leg_arti_list = [x for x in inventory_items if x["artifact"]["spec"]["rarity"] == "LEGENDARY"]

                any_no_id_leg = any(1 for x in leg_arti_list if not x["serverId"])
                backup_dict["not_auth_leg"]=True if any_no_id_leg else False


                any_duped_leg = any(x for x in leg_arti_list if x["quantity"] > 1)
                backup_dict["duped_leg"]=True if any_duped_leg else False

                any_ship_dupe = len(set([i["identifier"] for i in backup_dict["artifactsDb"]['missionArchive']])) != len([i["identifier"] for i in backup_dict["artifactsDb"]['missionArchive']])
                backup_dict["any_ship_dupe"] = True if any_ship_dupe else False

                count_l = int(sum(1 for x in inventory_items if x["artifact"]["spec"]["rarity"] == "LEGENDARY" and x["serverId"]))
                backup_dict["LLC_calculated"]={"valid":True,"value":count_l-expected_craft_l-expected_drop_l}
            except Exception as e:
                backup_dict["LLC_calculated"]={"valid":False,"value":"Invalid"}

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


def getLastReport(mongo):
    return mongo.get_last_report_legendary()

def getReportByDate(mongo, date):
    try:
        report=mongo.get_anonymus_legendary_report_by_date(date)
        return {"success": True, "message": report} if report is not None else {"success": False, "message": "There is no report for the specified date"}
    except Exception as e:
        return {"success": False, "message": e}

def getTimestampsReport(mongo):
    try:
        return {"success": True, "message": mongo.get_timestamps_legendary_report()}
    except Exception as e:
        return {"success": False, "message": e}