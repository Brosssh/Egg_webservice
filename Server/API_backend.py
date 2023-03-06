import datetime
import threading

from tqdm import tqdm
from datetime import timedelta
from Server import show_personal_leaderboard
from Server import insert_EID
from Server import show_leaderboard
from Server import utiliy
from Server.server_manager import server
import logging
from Server.ships_functions import update_leaderboard


def inizialize_EID(EID):
    server_manager = server()
    result = server_manager.get_bot_first_contact(EID)
    if not result:
        return False,{"success": False, "code": -3, "content": "Bad response by auxbrain"}
    checksum = result.backup.checksum
    if checksum == 0:
        return False,{"success": False, "code": -2, "content": "The EID is not registered in egg server"}
    return server_manager,result

def insert_eid_api(EID,mongo):
    if mongo is None:
        return {"success": False, "code": -4, "content": "Unable to contact mongo"}
    try:
        server_manager,result=inizialize_EID(EID)
        if not server_manager:
            return result
        name=result.backup.user_name
        encypted_EID=utiliy.encrypt_string(EID)
        do_exist=mongo.user_exists(encypted_EID)
        doc=mongo.get_full_from_eid(encypted_EID)
        if ("last_update_date" in doc.keys()):
            last_update_date=datetime.datetime.strptime(doc["last_update_date"],'%Y-%m-%d %H:%M:%S.%f')
            new_update_date=last_update_date+ timedelta(hours=1)
            if utiliy.datetime_now().timestamp() < new_update_date.timestamp():
                return {"success": False, "code": -5, "content": "You can submit your EID on "+str(new_update_date)}
        t=threading.Thread(target=insert_EID.insert,args=(server_manager,mongo,result,encypted_EID,do_exist))
        t.start()
        return {"success": True, "code": 1, "content": "Thanks "+name+", your ships are being updated... Check the leaderboard in a few minutes"} if do_exist is not None else {"success": True, "code": 2, "content": "Thanks for your submission "+name+". Since it's your first submission it will take some time, check back the leaderboard in some minutes"}
    except Exception as e:
        return {"success": False, "code": -1, "content": str(e)}


def get_leaderboard(mongo, element, n, top_n):
    logging.basicConfig(filename='getLeaderboard.log', level=logging.INFO)
    try:
        if element is None or n is None or top_n is None:
            return {"success": False, "code": 0, "content": "Malformed get"}
        if not n.isnumeric()  or not top_n.isnumeric():
            return {"success": False, "code": 0, "content": "Malformed get"}
        logging.info('Called get_leaderboard with parameter: '+str(element)+" : "+str(n)+" : "+str(top_n))
        if mongo is None:
            return {"success": False, "code": -4, "content": "Unable to contact mongo"}
        if str(element) not in utiliy.get_leaderboards_names_static():
            return {"success": False, "code": 0, "content": str(element)+" is not a valid leaderboard"}



        res=show_leaderboard.get_leader(mongo, str(element), int(n), int(top_n))
        if type(res) is not Exception:
            logging.info(
                'Get_leaderboard with parameter: ' + str(element) + " : " + str(
                    n) + " : " + str(top_n)+" returned OK")
            return {"success": True, "code": 1, "content": res}
        else:
            logging.warning(res)
            return {"success": False, "code": -1, "content": str(res)}
    except Exception as e:
        return {"success": False, "code": -1, "content": str(e)}


def get_personal_leaderboard(mongo, EID):
    try:
        if EID is None:
            return {"success": False, "code": 0, "content": "Please specify the EID"}
        if mongo is None:
            return {"success": False, "code": -4, "content": "Unable to contact mongo"}

        server_manager, result = inizialize_EID(EID)
        if not server_manager:
            return result
        encypted_EID=utiliy.encrypt_string(EID)
        if not mongo.user_exists(encypted_EID):
            return {"success": False, "code": -4, "content": "You need to first submit your EID in order to view your dashboard"}

        return {"success": True, "code": 1, "content": show_personal_leaderboard.calculate_pers_dash(mongo,encypted_EID)}

    except Exception as e:
        return {"success": False, "code": -1, "content": str(e)}

def debug_only_reset_leaderboards(mongo):
    only_value={"1":{'name': [], 'stars': [], 'capacity': [], 'identifier': [], 'count': [{'1': 0, '2': 0, '3': 0, '4': 0, 'total': 0}]}}
    for el in utiliy.get_leaderboards_names_static():
        mongo.load_updated_document_by_name(only_value,el)
    for encrypted_EID in tqdm([el["EID"] for el in list(mongo.get_all_encrypted_IDs())]):
        full_ships=mongo.get_full_from_eid(encrypted_EID)
        leaderboard_dict = mongo.build_full_leaderboard()
        print('Started leaderboard update EID : ' + encrypted_EID)
        leaderboard_updated = update_leaderboard(leaderboard_dict, full_ships)
        for el in leaderboard_updated:
            mongo.load_updated_document_by_name(leaderboard_updated[el], el)
