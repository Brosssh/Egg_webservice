from flask import Flask, request
from Server.mongoDB_manager import mongo_manager
from Server import new_EID


lines = open("conf.txt", "r").readlines()
user = lines[0].strip()
pssw = lines[1].strip()

conn = "mongodb+srv://" + user + ":" + pssw + "@eggcluster.sbrsi.mongodb.net/?retryWrites=true&w=majority"

mongo = mongo_manager(conn)

app = Flask(__name__)

@app.route('/sendNewEID', methods=["GET"])
def newEID():
    EID=str(request.args.get('EID'))
    response=new_EID.insert_eid_api(EID,mongo)
    return response

