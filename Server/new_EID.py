from Server import utiliy
from Server.server_manager import server


def insert_eid_api(EID,mongo):
    try:
        server_manager = server()
        result = server_manager.get_bot_first_contact(EID)
        checksum = result.backup.checksum
        if checksum == 0:
            return {"success":False,"code":-1,"content":""}
        else:
            name=result.backup.user_name
            return {"success": True, "code": 1, "content": name} if mongo.get_full_from_eid(utiliy.encrypt_string(EID))is not None else {"success": True, "code": 0, "content": name}
    except:
        return {"success": False, "code": -2, "content": ""}

