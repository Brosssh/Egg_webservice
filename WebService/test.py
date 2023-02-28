import socket
from threading import Thread
import select
from Server import new_EID
from Server.mongoDB_manager import mongo_manager
from requests.models import Response


lines = open("conf.txt", "r").readlines()
user = lines[0].strip()
pssw = lines[1].strip()

conn = "mongodb+srv://" + user + ":" + pssw + "@eggcluster.sbrsi.mongodb.net/?retryWrites=true&w=majority"

mongo = mongo_manager(conn)



class ClientThread(Thread):


    def __init__(self,ip,port):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        print("[+] New thread started for "+ip+":"+str(port))


    def run(self):
        while True:
            data = conn.recv(2048)
            if not data: break
            if data.__contains__(b"GET /sendNewEID?EID="):
                response=new_EID.insert_eid_api(data.split(b" ")[1].split(b"=")[1],mongo)
                print("response:", response)
                sting_response='''HTTP/1.0 200 OK
                Content-Type: text/plain

'''+str(response)+'''

                '''
                conn.send(bytes(sting_response, 'utf-8'))
                conn.close()

TCP_IP = '0.0.0.0'
TCP_PORT = 5000
BUFFER_SIZE = 1024
threads = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((TCP_IP, TCP_PORT))
server_socket.listen(10)

read_sockets, write_sockets, error_sockets = select.select([server_socket], [], [])

while True:
    print("Waiting for incoming connections...")
    for sock in read_sockets:
        (conn, (ip,port)) = server_socket.accept()
        newthread = ClientThread(ip,port)
        newthread.start()
        threads.append(newthread)
    for t in threads:
        t.join()