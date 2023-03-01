import os
from flask import Flask, request

from Server.mongoDB_manager import mongo_manager
from Server import API_backend


user=os.environ.get('user')
pssw=os.environ.get('pssw')

conn = "mongodb+srv://" + user + ":" + pssw + "@eggcluster.sbrsi.mongodb.net/?retryWrites=true&w=majority"

mongo = mongo_manager(conn)

app = Flask(__name__)

@app.route('/', methods=["GET"])
def main():
    return "test"


@app.route('/sendNewEID', methods=["GET"])
def newEID():
    EID=str(request.args.get('EID'))
    response=API_backend.insert_eid_api(EID,mongo)
    return response

@app.route('/getLeaderboard', methods=["GET"])
def getlead():
    element=request.args.get('element')
    n = request.args.get('n')
    top_n = request.args.get('top_n')
    response=API_backend.get_leaderboard(mongo,element,n,top_n)
    return response
