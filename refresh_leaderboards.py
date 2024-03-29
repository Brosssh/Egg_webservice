from Server import server_manager
from Server.mongoDB_manager import mongo_manager
from Server import API_backend
import os

user=os.getenv('MONGO_USER')
pssw=os.getenv('MONGO_PSSW')


conn = "mongodb+srv://" + user + ":" + pssw + "@eggcluster.sbrsi.mongodb.net/?retryWrites=true&w=majority"


mongo = mongo_manager(conn)
server=server_manager.server()

API_backend.debug_only_reset_leaderboards(mongo)

