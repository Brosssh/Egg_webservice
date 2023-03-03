import time

import utiliy
from concurrent.futures.thread import ThreadPoolExecutor

def call_script(result,arg,mongo,user_name):
    result.append(mongo.get_first_encounter(arg,user_name))



def multi_thread(result,mongo,user_name):
    with ThreadPoolExecutor(max_workers=34) as executor:
        ordinal = 1
        for arg in utiliy.get_leaderboards_names_static():
            executor.submit(call_script,result,arg,mongo,user_name)
            ordinal += 1
    return result

def calculate_pers_dash(mongo,encrypted_EID):
    pers_lead=[]
    user_name=mongo.get_name_by_EID(encrypted_EID)
    pers_lead2=multi_thread(pers_lead,mongo,user_name)
    return pers_lead2