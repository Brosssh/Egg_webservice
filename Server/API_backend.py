from Server import show_leaderboard
from Server import utiliy
from Server.server_manager import server

def insert_eid_api(EID,mongo):
    if mongo is None:
        return {"success": False, "code": -4, "content": "Unable to contact mongo"}
    try:
        server_manager = server()
        result = server_manager.get_bot_first_contact(EID)
        if not result:
            return {"success": False, "code": -3, "content": "Unable to contact egg server"}
        checksum = result.backup.checksum
        if checksum == 0:
            return {"success":False,"code":-1,"content":""}
        else:
            name=result.backup.user_name
            return {"success": True, "code": 1, "content": name} if mongo.get_full_from_eid(utiliy.encrypt_string(EID))is not None else {"success": True, "code": 0, "content": name}
    except Exception as e:
        return {"success": False, "code": -2, "content": str(e)}


def get_leaderboard(mongo, element, n, top_n):
    if mongo is None:
        return {"success": False, "code": -4, "content": "Unable to contact mongo"}
    if element is None or n is None or top_n is None:
        return {"success": False, "code": 0, "content": "Malformed get"}
    if str(element) not in utiliy.get_leaderboards_names_static():
        return {"success": False, "code": 0, "content": str(element)+" is not a valid leaderboard"}
    return {"success": True, "code": 1, "content": show_leaderboard.get_leader(mongo, str(element), int(n), int(top_n))}