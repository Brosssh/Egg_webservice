import threading

from flask import Flask, request
import os

from Server.API_backend import Compute
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


@app.route('/sendNewEID', methods=["POST"])
def newEID():
    EID_submit=request.form['EID']
    response=API_backend.get_message(EID_submit,mongo)
    if response["success"]:
        app.logger.info("Starting compute "+EID_submit)
        thread_a = Compute(EID_submit,mongo)
        thread_a.start()
    return response

@app.route('/getLeaderboard', methods=["GET"])
def getlead():
    element=request.args.get('element')
    n = request.args.get('n')
    top_n = request.args.get('top_n')
    response=API_backend.get_leaderboard(mongo,element,n,top_n)
    return response

@app.route('/getPersonalLeaderboard', methods=["GET"])
def getperslead():
    EID=request.args.get('EID')
    response=API_backend.get_personal_leaderboard(mongo,EID)
    return response
