def __get_leader_arrays_ingr__(mongo, obj, ship_num):
    header = ["Pos", "Name", "Stars", "Capacity", "T1", "T2", "T3", "Total " + obj]
    table = []
    leader_dict = mongo.get_leaderboard_by_name(obj)
    for i in range(1, (ship_num if ship_num < len(leader_dict["content"]) else len(leader_dict["content"])) + 1):
        this_list = []
        this_list.append(str(i))
        for sub_el in leader_dict["content"][str(i)]:
            for j in range(len(leader_dict["content"][str(i)]["name"])):
                if sub_el == "count":
                    for el in leader_dict["content"][str(i)][sub_el][j]:
                        this_list.append(str(j) + ":" + str(leader_dict["content"][str(i)][sub_el][j][el]))

                if sub_el != "identifier" and sub_el != "count" and sub_el != "name":
                    this_list.append(str(j) + ":" + str(leader_dict["content"][str(i)][sub_el][j]))

                if sub_el == "name":
                    this_list.append(str(j) + ":" + str(leader_dict["content"][str(i)][sub_el][j][:10]))

        for i in range(0, int((len(this_list) - 1) / 7)):
            l = [this_list[0]]
            for el in this_list[1:]:
                ident, content = el.split(":")
                if str(ident) == str(i):
                    l.append(content)
            table.append(l)

    return table, header


def __get_leader_arrays_stone__(mongo, obj, ship_num):
    header = ["Pos", "Name", "Stars", "Capacity", "T1", "T2", "T3", "T4", "Tot " + obj]
    table = []
    leader_dict = mongo.get_leaderboard_by_name(obj)
    for i in range(1, (ship_num if ship_num < len(leader_dict["content"]) else len(leader_dict["content"])) + 1):
        this_list = []
        this_list.append(str(i))
        for sub_el in leader_dict["content"][str(i)]:
            for j in range(len(leader_dict["content"][str(i)]["name"])):
                if sub_el == "count":
                    for el in leader_dict["content"][str(i)][sub_el][j]:
                        this_list.append(str(j) + ":" + str(leader_dict["content"][str(i)][sub_el][j][el]))

                if sub_el != "identifier" and sub_el != "count" and sub_el != "name":
                    this_list.append(str(j) + ":" + str(leader_dict["content"][str(i)][sub_el][j]))

                if sub_el == "name":
                    this_list.append(str(j) + ":" + str(leader_dict["content"][str(i)][sub_el][j][:10]))

        for i in range(0, int((len(this_list) - 1) / 8)):
            l = [this_list[0]]
            for el in this_list[1:]:
                ident, content = el.split(":")
                if str(ident) == str(i):
                    l.append(content)
            table.append(l)

    return table, header



# top n ships for users
def get_table_top_n(table, n):
    if n == 0:
        return table
    users = {}
    new_table = []
    for el in table:
        if el[1] in users.keys():
            if users[el[1]] < n:
                users[el[1]] += 1
                new_table.append(el)
        else:
            users[el[1]] = 1
            new_table.append(el)
    return new_table


def get_leader(mongo, obj, number, top_n):
    try:
        if obj == "gold" or obj == "titanium" or obj == "tau":
            table, header = __get_leader_arrays_ingr__(mongo, obj, number)
        else:
            table, header = __get_leader_arrays_stone__(mongo, obj, number)
        new_table = get_table_top_n(table, top_n)
        return new_table[:number]
    except Exception as e:
        return e


