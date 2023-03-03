#MONGO IS NOT THE OPTIMAL CHOICE, IK, BUT IT'S FREE SO I'LL USE IT
import copy

from bson import ObjectId
from pymongo import MongoClient

from Server import utiliy


class mongo_manager:

    client=None

    def __init__(self,conn_string):
        try:
            if self.client is None:
                self.client = MongoClient(conn_string)
        except:
            print("Something went wrong with the database connection")

    def __get_leaderboard_coll__(self):
        try:
            mydb = self.client["db_leaderboard"]
            mycol = mydb["leaderboard"]
            return mycol
        except:
            print("Something went wrong with the database connection")

    def __get_collection__(self):
        try:
            mydb = self.client["db_leaderboard"]
            mycol = mydb["users_ship"]
            return mycol
        except:
            print("Something went wrong with the database connection")

    def doc_by_name(self,name):
        try:
            return self.__get_collection__().find({"name":name})
        except Exception as e:
            print(e)

    def insert_full_user_ships(self,dict_to_insert):
        try:
            self.__get_collection__().insert_one(dict_to_insert)
        except Exception as e:
            print(e)

    def get_drop_by_name(self,name):
        path="ships.ship.drops."+name
        return self.__get_collection__().find({path:{"$exists":1}})


    def get_full_from_eid(self,eid):
        try:
            return self.__get_collection__().find_one({'EID':eid})
        except Exception as e:
            print(e)

    def user_exists(self, encryptedEID):
        try:
            res= self.__get_collection__().find_one({'EID':encryptedEID})
            if res is None:
                return False
            else:
                return True
        except Exception as e:
            print(e)

    def get_all_encrypted_IDs(self):
        array_id = self.__get_collection__().find({}, {"EID": 1})
        return array_id

    def get_ID_ships_already_stored(self,encryptedEID):
        ships = self.__get_collection__().find({"EID": encryptedEID}, {"ships": 1})
        list_already_stored = []
        for el in ships:
            for i in range(len(el["ships"])):
                list_already_stored.append(el["ships"][i]["identifier"])
        return list_already_stored

    def update_and_return_user_ships(self, final_dict, encryptedEID):
        list_already_stored=self.get_ID_ships_already_stored(encryptedEID)
        to_append=[]
        for el in final_dict["ships"]:
            if el["identifier"] not in list_already_stored:
                to_append.append(el)
        if len(to_append) > 0:
            print("Inserting "+str(len(to_append))+" new ships to the database")
            #get old doc
            doc=self.get_full_from_eid(encryptedEID)
            #contains a dict of only the new ships
            to_return=copy.deepcopy(doc)
            to_return["ships"]=to_return["ships"].clear()
            to_return["ships"]=[]
            for el in to_append:
                doc["ships"].append(el)
                to_return["ships"].append(el)
            self.__get_collection__().delete_one({"EID":encryptedEID})
            self.__get_collection__().insert_one(doc)
            return to_return
        else:
            print("No new ships")
            return None

    def get_leaderboard_stone_ingr(self):
        try:
            return self.__get_leaderboard_coll__().find_one({"_id":ObjectId("62bea7e7103e3eb4639db3ea")})
        except Exception as e:
            print(e)

    def load_updated_document(self, leaderboard_updated,id):
        try:
            self.__get_leaderboard_coll__().delete_one({"_id":id})
            self.__get_leaderboard_coll__().insert_one(leaderboard_updated)
            #print("Leaderboard updated")
        except Exception as e:
            print(e)

    def load_updated_document_by_name(self, leaderboard_updated,name):
        try:
            self.__get_leaderboard_coll__().delete_one({"name":name})
            self.__get_leaderboard_coll__().insert_one({"name":name,"content":leaderboard_updated})
        except Exception as e:
            print(e)

    def get_leaderboard_test(self):
        try:
            return self.__get_leaderboard_coll__().find_one({"type": "artifacts"})
        except Exception as e:
            print(e)

    def build_full_leaderboard(self):
        try:
            all_docs=[el for el in self.__get_leaderboard_coll__().find({"name":{"$exists":1}})]
            big_dict={}
            for el in all_docs:
                big_dict[el["name"]]=el["content"]
            return big_dict
        except Exception as e:
            print(e)

    def get_leaderboard_by_name(self,name):
        try:
            return self.__get_leaderboard_coll__().find_one({"name": name})
        except Exception as e:
            print(e)

    def get_leaderboards_names(self):
        try:
            l=self.__get_leaderboard_coll__().find()
            return [el["name"] for el in l]
        except Exception as e:
            print(e)

    def insert_clear_leaderboard(self):
        self.__get_leaderboard_coll__().delete_many({})
        try:
            for el in ["gold","tau","titanium"]:
                self.__get_leaderboard_coll__().insert_one(
                    {"name": el, "content": {"1": {"name": [],"stars": [],"capacity": [],"identifier": [],"count": [{"1": 0,"2":0,"3": 0,"total": 0}]}}}
)
            for el in ["clarity", "lunar", "prophecy", "life", "quantum", "dilithium",
                "soul", "terra", "tachyon", "shell"]:
                self.__get_leaderboard_coll__().insert_one(
                    {"name": el, "content": {"1": {"name": [],"stars": [],"capacity": [],"identifier": [],"count": [{"1": 0,"2":0,"3": 0,"4": 0,"total": 0}]}}})

            for el in utiliy.get_ingame_input_artis()[1]:
                self.__get_leaderboard_coll__().insert_one(
                    {"name": el, "content": {"1": {"name": [], "stars": [], "capacity": [], "identifier": [],
                                                   "count": [{"1": 0, "2": 0, "3": 0, "4": 0, "total": 0}]}}})

        except Exception as e:
            print(e)

    def get_name_by_EID(self,EID):
        return self.__get_collection__().find_one({"EID": EID}, {"name": 1})["name"]

    def get_first_encounter(self,el,user_name):
        print("Start " + el)
        leaderboard=self.__get_leaderboard_coll__().find_one({"name":el})["content"]
        result=[]
        print("Leaderboard "+el+ " retrieved from mongo")
        for i in range(len(leaderboard)+1):
            if user_name in leaderboard[str(i+1)]["name"]:
                for j in range(len(leaderboard[str(i+1)]["name"])):
                    if leaderboard[str(i+1)]["name"][j]==user_name:
                        result.append(el)
                        result.append(str(i+1))
                        for key  in leaderboard[str(i+1)].keys():
                            if key!="identifier" and key!="count":
                                result.append(leaderboard[str(i+1)][key][j])
                            if key=="count":
                                for count_el in leaderboard[str(i+1)][key][j].values():
                                    result.append(str(count_el))
                        print("Finish " + el)
                        return result
