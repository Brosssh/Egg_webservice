from google.protobuf.json_format import MessageToJson, MessageToDict
import copy

from Server import utiliy


def __get_array_ships_ID__(res): #get all exthens IDs
    ships = res.backup.artifacts_db.mission_archive
    return [el.identifier for el in ships if "HENERPRISE" in str(el) and "EPIC" in str(el) and "ARCHIVED" in str(el)]


def loots(res,server_manager, mongo, encryptedEID):
    file_loot=[]
    already_stored_IDS=mongo.get_ID_ships_already_stored(encryptedEID)
    new_ships=[el for el in __get_array_ships_ID__(res) if el not in already_stored_IDS]
    #print("Please wait, DO NOT CLOSE THIS PAGE, maybe you can actually but please wait till the end and don't press STOP :)\n")
    #print("If you are wondering why it's this slow it's because i don't want to spend some money on a server so replit is doing the job\n\n")
    n=0
    for el in new_ships:
        try:
            ship_raw = server_manager.get_loot(el)
            ship_dict=(MessageToDict(ship_raw.info))
            n_drops=len(ship_raw.artifacts)
            drops=[]
            for i in range(n_drops):
                dict_temp=MessageToDict(ship_raw.artifacts[i])
                drops.append(dict_temp)
            ship_dict["drop_List"]=drops
            file_loot.append(ship_dict)
        except Exception as e:
            print(e)

    return file_loot

def __level_to_tier__(name, level_string):
    if "STONE" in name:
        if "FRAGMENT" in name:
            return 1
        elif level_string=="INFERIOR":
            return 2
        elif level_string == "LESSER":
            return 3
        elif level_string=="NORMAL":
            return 4
    else:
        return 1 if level_string=="INFERIOR" else 2 if level_string=="LESSER" \
            else 3 if level_string=="NORMAL" else 4 if level_string=="GREATER" else 0

def semplify_drop_list(list_drop):
    drops={}
    for el in list_drop:
        name=el["spec"]["name"]
        level=el["spec"]["level"]
        rarity=el["spec"]["rarity"]
        tier=str(__level_to_tier__(name,level))
        if name not in drops.keys():
            drops[name]={tier: {rarity:{"count":1}}}
        elif tier not in drops[name].keys():
            drops[name][tier] = {rarity:{"count":1}}
        elif rarity not in drops[name][tier].keys():
            drops[name][tier][rarity] = {"count":1}
        else:
            drops[name][tier][rarity]["count"]+=1
    return drops

def semplify_dict(file_dict):
    new_dict=[]
    for el in file_dict:
        identifier=el["identifier"]
        capacity = el["capacity"]
        stars=0
        try:
            stars=el["level"]
        except:
            pass
        drops=el["drop_List"]
        semplified_drops=semplify_drop_list(drops)
        new_dict.append({"identifier":identifier,"stars":stars,"capacity":capacity, "drops":semplified_drops})
    return new_dict


################################################################################
#To build the leaderboard
def check_if_same_total(leaderboard,current_el):
    done_something=False
    for pos in [str(el) for el in range(1,len(leaderboard)+1)]:
        if leaderboard[pos]["count"][0]["total"] == current_el["count"]["total"]:
            for sub_el in current_el:
                leaderboard[pos][sub_el].append(current_el[sub_el])
            done_something=True
    return leaderboard, done_something


def move_all_down(start,current_el,leaderboard):
    leaderboard[str(len(leaderboard)+1)]=copy.deepcopy(leaderboard[str(len(leaderboard))])
    for i in range(len(leaderboard),int(start),-1):
        leaderboard[str(i)]=copy.deepcopy(leaderboard[str(i-1)])
    for sub_el in current_el:
        leaderboard[start][sub_el].clear()
        leaderboard[start][sub_el].append(copy.deepcopy(current_el[sub_el]))
    return leaderboard


def check_if_beetween_total(leaderboard,current_el):
    for pos in [str(el) for el in range(1, len(leaderboard) + 1)]:
        if current_el["count"]["total"]>leaderboard[pos]["count"][0]["total"]:
            move_all_down(pos,current_el,leaderboard)
            break

    #new last
    if current_el["count"]["total"] < leaderboard[str(len(leaderboard))]["count"][0]["total"]:
        leaderboard[str(len(leaderboard) + 1)] = copy.deepcopy(leaderboard[str(len(leaderboard))])
        for sub_el in current_el:
            leaderboard[str(len(leaderboard))][sub_el].clear()
            leaderboard[str(len(leaderboard))][sub_el].append(copy.deepcopy(current_el[sub_el]))
    return leaderboard


def check_and_update_file(old_leadberboard_l_dict,array_new_ingr):
    new_leaderboard_l_dict=old_leadberboard_l_dict
    array_new_ingr=sorted(array_new_ingr, key = lambda item: item['count']['total'])
    for el in array_new_ingr:
        new_leaderboard_l_dict,done_something=check_if_same_total(new_leaderboard_l_dict,el)
        #if i have already found a number with same total i don't need to check if it's between
        if not done_something:
            new_leaderboard_l_dict = check_if_beetween_total(new_leaderboard_l_dict, el)
    return new_leaderboard_l_dict

def ingredients(old_leaderboard_l_dict,new_ships,ingr_name):
    array_ing_new=[]
    user=new_ships["name"]
    for el in new_ships["ships"]:
        ingr_dict = dict({"count":{"1": 0, "2": 0, "3": 0, "total": 0},"stars":0,"name":"","capacity": 0})
        for singol_drop in el["drops"]:
            if singol_drop==ingr_name:
                ingr_dict["stars"] = el["stars"]
                ingr_dict["name"] = user
                ingr_dict["capacity"] = el["capacity"]
                ingr_dict["identifier"] = el["identifier"]
                for number in el["drops"][ingr_name]:
                    ingr_dict["count"][number]+=el["drops"][ingr_name][number]["COMMON"]["count"]

        #total is calculated at t1 + (t2 * t1_required for a t2) + (t3 * t2_required for a t3)

        #example 1 t1 gold, 5 t2 gold, and 3 t3 gold are (1) + (5*9) + (3*9*11)
        #since a t2 is made with 9 t1 and a t3 is made with 11 t2
        t2_mult= 9 if ingr_name == "GOLD_METEORITE" else 12 if ingr_name =="TAU_CETI_GEODE" else \
            10 if ingr_name =="SOLAR_TITANIUM" else 0
        t3_mult=t2_mult*(11 if ingr_name == "GOLD_METEORITE" else 14 if ingr_name =="TAU_CETI_GEODE"
            else 12 if ingr_name =="SOLAR_TITANIUM" else 0)


        ingr_dict["count"]["total"]=ingr_dict["count"]["1"]+(ingr_dict["count"]["2"]*t2_mult)+(ingr_dict["count"]["3"]*t3_mult)
        if ingr_dict["count"]["total"] > 0:
            array_ing_new.append(ingr_dict)

    return check_and_update_file(old_leaderboard_l_dict,array_ing_new)

def stones(old_leaderboard_l_dict,new_ships,stone_name):
    array_stone_new=[]
    user=new_ships["name"]
    for el in new_ships["ships"]:
        stone_dict = dict({"count":{"1": 0, "2": 0, "3": 0,"4":0,"total": 0},"stars":0,"name":"","capacity": 0})
        for singol_drop in el["drops"]:
            if singol_drop==stone_name:
                stone_dict["stars"] = el["stars"]
                stone_dict["name"] = user
                stone_dict["capacity"] = el["capacity"]
                stone_dict["identifier"] = el["identifier"]
                for number in el["drops"][stone_name]:
                    stone_dict["count"][number]+=el["drops"][stone_name][number]["COMMON"]["count"]
            frag_name=stone_name + "_FRAGMENT"
            if singol_drop == frag_name:
                stone_dict["stars"] = el["stars"]
                stone_dict["name"] = user
                stone_dict["capacity"] = el["capacity"]
                stone_dict["identifier"] = el["identifier"]
                for number in el["drops"][frag_name]:
                    stone_dict["count"][number]+=el["drops"][frag_name][number]["COMMON"]["count"]


        t2_mult= 20 #every t2 is made with 20 t1
        t3_mult=t2_mult*(
            10 if stone_name == "CLARITY_STONE" else
            20 if stone_name == "LUNAR_STONE" else
            10 if stone_name == "PROPHECY_STONE" else
            12 if stone_name == "LIFE_STONE" else
            15 if stone_name == "QUANTUM_STONE" else
            12 if stone_name == "DILITHIUM_STONE" else
            15 if stone_name == "SOUL_STONE" else
            15 if stone_name == "TERRA_STONE" else
            15 if stone_name == "TACHYON_STONE" else
            20 if stone_name == "SHELL_STONE" else
            0)
        t4_mult = t3_mult * (
            20 if stone_name == "CLARITY_STONE" else
            25 if stone_name == "LUNAR_STONE" else
            12 if stone_name == "PROPHECY_STONE" else
            15 if stone_name == "LIFE_STONE" else
            20 if stone_name == "QUANTUM_STONE" else
            15 if stone_name == "DILITHIUM_STONE" else
            20 if stone_name == "SOUL_STONE" else
            20 if stone_name == "TERRA_STONE" else
            20 if stone_name == "TACHYON_STONE" else
            10 if stone_name == "SHELL_STONE" else
                0)

        stone_dict["count"]["total"]=stone_dict["count"]["1"]+(stone_dict["count"]["2"]*t2_mult)+(stone_dict["count"]["3"]*t3_mult)+(stone_dict["count"]["4"]*t4_mult)
        if stone_dict["count"]["total"] > 0:
            array_stone_new.append(stone_dict)

    return check_and_update_file(old_leaderboard_l_dict,array_stone_new)

def artifacts(old_leaderboard_l_dict,new_ships,arti_name):
    array_arti_new=[]
    user=new_ships["name"]
    for el in new_ships["ships"]:
        arti_dict = dict({"count":{"1": 0, "2": 0, "3": 0,"4":0,"total": 0},"stars":0,"name":"","capacity": 0})
        for singol_drop in el["drops"]:
            if singol_drop==arti_name:
                arti_dict["stars"] = el["stars"]
                arti_dict["name"] = user
                arti_dict["capacity"] = el["capacity"]
                arti_dict["identifier"] = el["identifier"]
                for number in el["drops"][arti_name]:
                    for rarity in el["drops"][arti_name][number]:
                        arti_dict["count"][number]+=el["drops"][arti_name][number][rarity]["count"]

        t2_mult= \
            6 if arti_name =="BOOK_OF_BASAN" else 5 if arti_name =="LIGHT_OF_EGGENDIL" else 6 if arti_name =="TACHYON_DEFLECTOR" else\
            6 if arti_name =="SHIP_IN_A_BOTTLE" else 4 if arti_name =="TITANIUM_ACTUATOR" else 5 if arti_name =="DILITHIUM_MONOCLE" else \
            5 if arti_name =="QUANTUM_METRONOME" else 6 if arti_name =="PHOENIX_FEATHER" else 4 if arti_name =="THE_CHALICE" else \
            6 if arti_name =="INTERSTELLAR_COMPASS" else 5 if arti_name =="CARVED_RAINSTICK" else 4 if arti_name =="BEAK_OF_MIDAS" else \
            6 if arti_name == "MERCURYS_LENS" else 4 if arti_name == "NEODYMIUM_MEDALLION" else 5 if arti_name == "ORNATE_GUSSET" else \
            6 if arti_name == "TUNGSTEN_ANKH" else 5 if arti_name == "AURELIAN_BROOCH" else 5 if arti_name == "VIAL_MARTIAN_DUST" else \
            3 if arti_name == "DEMETERS_NECKLACE" else 3 if arti_name == "LUNAR_TOTEM" else 3 if arti_name == "PUZZLE_CUBE" else 0
        t3_mult=t2_mult*(
            10 if arti_name == "BOOK_OF_BASAN" else 7 if arti_name == "LIGHT_OF_EGGENDIL" else 10 if arti_name == "TACHYON_DEFLECTOR" else
            9 if arti_name == "SHIP_IN_A_BOTTLE" else 6 if arti_name == "TITANIUM_ACTUATOR" else 8 if arti_name == "DILITHIUM_MONOCLE" else
            7 if arti_name == "QUANTUM_METRONOME" else 10 if arti_name == "PHOENIX_FEATHER" else 6 if arti_name == "THE_CHALICE" else
            8 if arti_name == "INTERSTELLAR_COMPASS" else 7 if arti_name == "CARVED_RAINSTICK" else 5 if arti_name == "BEAK_OF_MIDAS" else
            8 if arti_name == "MERCURYS_LENS" else 5 if arti_name == "NEODYMIUM_MEDALLION" else 6 if arti_name == "ORNATE_GUSSET" else
            7 if arti_name == "TUNGSTEN_ANKH" else 7 if arti_name == "AURELIAN_BROOCH" else 7 if arti_name == "VIAL_MARTIAN_DUST" else
            5 if arti_name == "DEMETERS_NECKLACE" else 6 if arti_name == "LUNAR_TOTEM" else 7 if arti_name == "PUZZLE_CUBE" else 0
        )
        t4_mult = t3_mult * (
            12 if arti_name == "BOOK_OF_BASAN" else 10 if arti_name == "LIGHT_OF_EGGENDIL" else 12 if arti_name == "TACHYON_DEFLECTOR" else
            12 if arti_name == "SHIP_IN_A_BOTTLE" else 8 if arti_name == "TITANIUM_ACTUATOR" else 10 if arti_name == "DILITHIUM_MONOCLE" else
            9 if arti_name == "QUANTUM_METRONOME" else 12 if arti_name == "PHOENIX_FEATHER" else 8 if arti_name == "THE_CHALICE" else
            10 if arti_name == "INTERSTELLAR_COMPASS" else 9 if arti_name == "CARVED_RAINSTICK" else 6 if arti_name == "BEAK_OF_MIDAS" else
            10 if arti_name == "MERCURYS_LENS" else 6 if arti_name == "NEODYMIUM_MEDALLION" else 8 if arti_name == "ORNATE_GUSSET" else
            8 if arti_name == "TUNGSTEN_ANKH" else 10 if arti_name == "AURELIAN_BROOCH" else 8 if arti_name == "VIAL_MARTIAN_DUST" else
            6 if arti_name == "DEMETERS_NECKLACE" else 6 if arti_name == "LUNAR_TOTEM" else 10 if arti_name == "PUZZLE_CUBE" else 0
        )

        arti_dict["count"]["total"]=arti_dict["count"]["1"]+(arti_dict["count"]["2"]*t2_mult)+(arti_dict["count"]["3"]*t3_mult)+(arti_dict["count"]["4"]*t4_mult)
        if arti_dict["count"]["total"] > 0:
            array_arti_new.append(arti_dict)

    return check_and_update_file(old_leaderboard_l_dict,array_arti_new)

def update_leaderboard(old_leaderboard_dict,new_ships):
    old_leaderboard_dict["gold"]=(ingredients(old_leaderboard_dict["gold"],new_ships,"GOLD_METEORITE"))
    old_leaderboard_dict["tau"] = (ingredients(old_leaderboard_dict["tau"], new_ships, "TAU_CETI_GEODE"))
    old_leaderboard_dict["titanium"] = (ingredients(old_leaderboard_dict["titanium"], new_ships, "SOLAR_TITANIUM"))

    stones_array=["CLARITY_STONE","LUNAR_STONE","PROPHECY_STONE","LIFE_STONE","QUANTUM_STONE","DILITHIUM_STONE","SOUL_STONE","TERRA_STONE","TACHYON_STONE","SHELL_STONE"]
    for el in stones_array:
        old_leaderboard_dict[el.split("_")[0].lower()] = (stones(old_leaderboard_dict[el.split("_")[0].lower()], new_ships, el))

    ingame, coll_name = utiliy.get_ingame_input_artis()
    for i in range(len(utiliy.get_ingame_input_artis()[0])):
        old_leaderboard_dict[coll_name[i]] = (artifacts(old_leaderboard_dict[coll_name[i]], new_ships, ingame[i]))

    return old_leaderboard_dict

################################################################################

