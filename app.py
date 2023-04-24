import threading

from flask import Flask, request
import os

from Server.mongoDB_manager import mongo_manager
from Server import API_backend as LB_backend

from LegendaryStudy import API_backend as LS_backend
from LegendaryStudy.mongoDB_manager import mongo_manager as LS_mongo_manager


#<editor-fold desc="Mongo connection for leaderboard stuff">
user=os.getenv('MONGO_USER')
pssw=os.getenv('MONGO_PSSW')


conn = "mongodb+srv://" + user + ":" + pssw + "@eggcluster.sbrsi.mongodb.net/?retryWrites=true&w=majority"

mongo = mongo_manager(conn)
#</editor-fold>

#<editor-fold desc="Mongo connection for legendary study etc">
LS_mongo = LS_mongo_manager()
mongo_reports=LS_mongo_manager(host="reports.dj5tz2b.mongodb.net")
#</editor-fold>

app = Flask(__name__)


@app.route('/', methods=["GET"])
def main():
    return "test"


@app.route('/sendNewEID', methods=["POST"])
def newEID():
    return "Submit on replit"

@app.route('/getLeaderboard', methods=["GET"])
def getlead():
    element=request.args.get('element')
    n = request.args.get('n')
    top_n = request.args.get('top_n')
    response=LB_backend.get_leaderboard(mongo,element,n,top_n)
    return response

@app.route('/getPersonalLeaderboard', methods=["GET"])
def getperslead():
    EID=request.args.get('EID')
    response=LB_backend.get_personal_leaderboard(mongo,EID)
    return response


@app.route('/submitEID', methods=["POST"])
def submitEID():
    EID=request.form.get('EID')
    response=LS_backend.submitEID(LS_mongo,EID)
    return response

@app.route('/getReportByDate', methods=["GET"])
def getReportByDate():
    date = int(request.args.get('date'))
    response=str(LS_backend.getReportByDate(mongo_reports,date)).replace('"', "'")
    return response

@app.route('/getTimestampsReport', methods=["GET"])
def getTimestampsReport():
    response=str(LS_backend.getTimestampsReport(mongo_reports)).replace('"', "'")
    return response
