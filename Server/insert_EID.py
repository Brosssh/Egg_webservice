import logging

from Server.ships_functions import loots, semplify_dict, update_leaderboard
from Server import utiliy


def insert(server,mongo,result,encrypted_EID,do_exist):
    try:
        loot_dict = loots(result, server, mongo, encrypted_EID)
        dict_loots = semplify_dict(loot_dict)
        final_dict = {"EID": encrypted_EID, "name": result.backup.user_name, "ships": dict_loots,"last_update_date":str(utiliy.datetime_now())}
        new_ships = final_dict
        if not do_exist:
            mongo.insert_full_user_ships(final_dict)
        else:
            new_ships = mongo.update_and_return_user_ships(final_dict, encrypted_EID)

        if new_ships is not None:
            leaderboard_dict = mongo.build_full_leaderboard()
            leaderboard_updated = update_leaderboard(leaderboard_dict, new_ships)
            for el in leaderboard_updated:
                mongo.load_updated_document_by_name(leaderboard_updated[el], el)
    except Exception as e:
        logging.critical("Something went wrong with EID "+encrypted_EID+"\n"+str(e))
