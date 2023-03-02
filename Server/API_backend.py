import threading
from Server import insert_EID
from Server import show_leaderboard
from Server import utiliy
from Server.server_manager import server
import logging


def insert_eid_api(EID,mongo):
    if mongo is None:
        return {"success": False, "code": -4, "content": "Unable to contact mongo"}
    try:
        server_manager = server()
        result = server_manager.get_bot_first_contact(EID)
        if not result:
            return {"success": False, "code": -3, "content": "EID not present on the server"}
        checksum = result.backup.checksum
        if checksum == 0:
            return {"success":False,"code":-2,"content":"EID is not valid for some reason"}
        else:
            name=result.backup.user_name
            encypted_EID=utiliy.encrypt_string(EID)
            do_exist=mongo.user_exists(encypted_EID)
            t=threading.Thread(target=insert_EID.insert,args=(server_manager,mongo,result,encypted_EID,do_exist))
            t.start()
            return {"success": True, "code": 1, "content": "Thanks "+name+", your ships are being updated... Check the leaderboard in a couple of minutes"} if do_exist is not None else {"success": True, "code": 2, "content": "Thanks for your submission "+name+". Since it's your first submission it will take some time, check back the leaderboard in some minutes"}
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