from mongoDB_manager import mongo_manager
from server_manager import server

if __name__ == '__main__':
    lines = open("WebService/conf.txt", "r").readlines()
    user = lines[0].strip()
    pssw = lines[1].strip()

    conn = "mongodb+srv://" + user + ":" + pssw + "@eggcluster.sbrsi.mongodb.net/?retryWrites=true&w=majority"

    mongo = mongo_manager(conn)
    server=server()