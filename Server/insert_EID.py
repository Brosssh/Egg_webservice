import logging
import datetime

from Server.ships_functions import loots, semplify_dict, update_leaderboard


def insert(server,mongo,result,encrypted_EID,do_exist):
    try:
        logging.info('Started insert EID process: ' + encrypted_EID + " ,exist: " + str(do_exist))
        loot_dict = loots(result, server, mongo, encrypted_EID)
        dict_loots = semplify_dict(loot_dict)
        logging.info('New ships for EID : ' + encrypted_EID + " ,ships: " + str(len(dict_loots)))
        print('New ships for EID : ' + encrypted_EID + " ,ships: " + str(len(dict_loots)))
        final_dict = {"EID": encrypted_EID, "name": result.backup.user_name, "ships": dict_loots,"last_update_date":str(datetime.datetime.now())}
        new_ships = final_dict
        if not do_exist:
            mongo.insert_full_user_ships(final_dict)
            logging.info('Inserted new doc EID : ' + encrypted_EID)
            print('Inserted new doc EID : ' + encrypted_EID)
        else:
            new_ships = mongo.update_and_return_user_ships(final_dict, encrypted_EID)
            logging.info('Updated doc EID : ' + encrypted_EID)
            print('Updated doc EID : ' + encrypted_EID)

        if new_ships is not None:
            leaderboard_dict = mongo.build_full_leaderboard()
            logging.info('Started leaderboard update EID : ' + encrypted_EID)
            print('Started leaderboard update EID : ' + encrypted_EID)
            leaderboard_updated = update_leaderboard(leaderboard_dict, new_ships)
            for el in leaderboard_updated:
                mongo.load_updated_document_by_name(leaderboard_updated[el], el)
            logging.info('Leaderboard update finished OK EID : ' + encrypted_EID)
            logging.info('Leaderboard update finished OK EID : ' + encrypted_EID)
            print('Leaderboard update finished OK EID : ' + encrypted_EID)
    except Exception as e:
        logging.critical("Something went wrong with EID "+encrypted_EID+"\n"+str(e))