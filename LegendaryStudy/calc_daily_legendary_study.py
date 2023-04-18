import copy

from tqdm import tqdm

from LegendaryStudy.mongoDB_manager import mongo_manager

def get_dict_legendary_players(file_list):
    final_dict_legendary = {}
    for el in tqdm(file_list):
        user_name=el["backup"]["userName"] if el["backup"]["userName"] is not None else "No alias"
        inventory_items = el["backup"]["artifactsDb"]["inventoryItems"]
        count = int(sum(x["quantity"] for x in inventory_items if x["artifact"]["spec"]["rarity"] == "LEGENDARY"))
        if str(count) in final_dict_legendary.keys():
            final_dict_legendary[str(count)].append(user_name)
        else:
            final_dict_legendary[str(count)] = [user_name]
    return final_dict_legendary

def get_zlc_record(file_list):
    result={}
    max_exthens=0
    for el in tqdm(file_list):
        inventory_items = el["backup"]["artifactsDb"]["inventoryItems"]
        user_name=el["backup"]["userName"] if el["backup"]["userName"] is not None else "No alias"
        count = int(sum(x["quantity"] for x in inventory_items if x["artifact"]["spec"]["rarity"] == "LEGENDARY"))
        if count==0:
            if "HENERPRISE:EPIC" in el["backup"]["artifactsDb"]["shipsCountArchiveAR"]:
                count_exthens=el["backup"]["artifactsDb"]["shipsCountArchiveAR"]["HENERPRISE:EPIC"]
                if count_exthens > max_exthens:
                    result={max_exthens:user_name}
    return result

def legendary_seen(file_list):
    leg_seen={}
    for x in tqdm(file_list):
        inventory_items = x["backup"]["artifactsDb"]["inventoryItems"]
        user_name=x["backup"]["userName"] if x["backup"]["userName"] is not None else "No alias"
        for el in inventory_items:
            if el["artifact"]["spec"]["rarity"] == "LEGENDARY":
                if el["artifact"]["spec"]["name"]+"_"+el["artifact"]["spec"]["level"] in leg_seen:
                    leg_seen[el["artifact"]["spec"]["name"]+"_"+el["artifact"]["spec"]["level"]].append(user_name)
                else:
                    leg_seen[el["artifact"]["spec"]["name"] + "_" + el["artifact"]["spec"]["level"]] = [user_name]
    return leg_seen


final_dict_report={}
mongo = mongo_manager()

file_list = mongo.get_users_files()
final_dict_report["leg_seen"]=legendary_seen(copy.deepcopy(file_list))
final_dict_report["legendary_players"]=get_dict_legendary_players(copy.deepcopy(file_list))
final_dict_report["zlc_record"]=get_zlc_record(copy.deepcopy(file_list))



print(final_dict_report)