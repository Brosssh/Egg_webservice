def unpack_position(group,pos):
    l=[]
    for i in range(len(group["name"])):
        this_l=[]
        this_l.append(str(pos))
        for key,val in group.items():
            if key!="count" and key!="identifier":
                this_l.append(val[i])
            elif key=="count":
                for key2,val2 in group[key][i].items():
                    this_l.append(val2)
        l.append(this_l)
    return l



def __get_leader_arrays_ingr__(mongo, obj, ship_num,top_n):
    header = ["Pos", "Name", "Stars", "Capacity", "T1", "T2", "T3", "Total " + obj]
    table = []
    leader_dict = mongo.get_leaderboard_by_name(obj)
    names_count = {}
    for pos in leader_dict["content"]:
        for el in unpack_position(leader_dict["content"][pos], pos):
            if is_name_valid(el[1], names_count, top_n):
                table.append(el)
                if len(table) == ship_num:
                    return table, header

    return table, header


def is_name_valid(curr_name,names_count, top_n):
    if top_n==0:
        return True
    if curr_name not in names_count.keys():
        names_count[curr_name]=1
        return True
    else:
        if names_count[curr_name]>=top_n:
            return False
        else:
            names_count[curr_name]+=1
            return True


def __get_leader_arrays_stone__(mongo, obj, ship_num,top_n):
    header = ["Pos", "Name", "Stars", "Capacity", "T1", "T2", "T3", "T4", "Tot " + obj]
    table = []
    leader_dict = mongo.get_leaderboard_by_name(obj)
    names_count={}
    for pos in leader_dict["content"]:
        for el in unpack_position(leader_dict["content"][pos],pos):
            if is_name_valid(el[1],names_count,top_n):
                table.append(el)
                if len(table) == ship_num:
                    return table,header

    return table, header


def get_leader(mongo, obj, number, top_n):
    try:
        if obj == "gold" or obj == "titanium" or obj == "tau":
            table, header = __get_leader_arrays_ingr__(mongo, obj, number,top_n)
        else:
            table, header = __get_leader_arrays_stone__(mongo, obj, number,top_n)
        return table
    except Exception as e:
        return e


