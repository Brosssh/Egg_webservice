import copy
import datetime
from tqdm import tqdm

from mongoDB_manager import mongo_manager

def get_dict_legendary_players(file_list):
    print("Starting get_dict_legendary_players")
    final_dict_legendary = {}
    for el in tqdm(file_list):
        try:
            user_name=el["backup"]["userName"] if el["backup"]["userName"] is not None else "No alias"
            inventory_items = el["backup"]["artifactsDb"]["inventoryItems"]
            count = int(sum(x["quantity"] for x in inventory_items if x["artifact"]["spec"]["rarity"] == "LEGENDARY"))
            if str(count) in final_dict_legendary.keys():
                final_dict_legendary[str(count)].append(user_name)
            else:
                final_dict_legendary[str(count)] = [user_name]
        except Exception as e:
            print("Exception while calculating get_dict_legendary_players for " + el["backup"]["eiUserId"] + ": " + str(e))
    print("Finish get_dict_legendary_players")
    return final_dict_legendary

def get_zlc_record(file_list, old_zlc_record):
    print("Starting get_zlc_record")
    if len(old_zlc_record)==1:
        max_exthens = int(list(old_zlc_record.keys())[0])
    else:
        max_exthens = 0
    result=old_zlc_record
    for el in tqdm(file_list):
        try:
            inventory_items = el["backup"]["artifactsDb"]["inventoryItems"]
            user_name=el["backup"]["userName"] if el["backup"]["userName"] is not None else "No alias"
            count = int(sum(x["quantity"] for x in inventory_items if x["artifact"]["spec"]["rarity"] == "LEGENDARY"))
            if count==0:
                if "HENERPRISE:EPIC" in el["backup"]["artifactsDb"]["shipsCountArchiveAR"]:
                    count_exthens=el["backup"]["artifactsDb"]["shipsCountArchiveAR"]["HENERPRISE:EPIC"]
                    if count_exthens > max_exthens:
                        max_exthens=count_exthens
                        result={str(max_exthens):{"user_name":user_name,"report_date":str(datetime.date.today())}}
        except Exception as e:
            print("Exception while calculating get_zlc_record for "+el["backup"]["eiUserId"]+": "+str(e))
    print("Finish get_zlc_record")
    return result

def legendary_seen(file_list):
    leg_seen={}
    print("Starting legendary_seen")
    for x in tqdm(file_list):
        try:
            inventory_items = x["backup"]["artifactsDb"]["inventoryItems"]
            user_name=x["backup"]["userName"] if x["backup"]["userName"] is not None else "No alias"
            for el in inventory_items:
                if el["artifact"]["spec"]["rarity"] == "LEGENDARY":
                    if el["artifact"]["spec"]["name"]+"_"+el["artifact"]["spec"]["level"] in leg_seen:
                        leg_seen[el["artifact"]["spec"]["name"]+"_"+el["artifact"]["spec"]["level"]].append(user_name)
                    else:
                        leg_seen[el["artifact"]["spec"]["name"] + "_" + el["artifact"]["spec"]["level"]] = [user_name]
        except Exception as e:
            print("Exception while calculating legendary_seen for "+x["backup"]["eiUserId"]+": "+str(e))
    print("Finish legendary_seen")
    return leg_seen


final_dict_report={}
mongo = mongo_manager()
mongo_reports = mongo_manager(host="reports.dj5tz2b.mongodb.net")
old_file=mongo_reports.get_last_report_legendary()

file_list = mongo.get_users_files()
final_dict_report["leg_seen"]=legendary_seen(copy.deepcopy(file_list))
final_dict_report["legendary_players"]=get_dict_legendary_players(copy.deepcopy(file_list))
final_dict_report["zlc_record"]=get_zlc_record(copy.deepcopy(file_list),old_file["report"]["zlc_record"])
final_dict_report["number_total_users"]=len(list(file_list))

print("Loading new report, "+str(datetime.date.today()))
mongo_reports.load_daily_report_legendary(final_dict_report)
print("New report loaded")
