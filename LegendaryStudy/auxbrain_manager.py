import Server.proto.ei_pb2 as ei_pb2
import base64
import requests


class auxbrain:

    EID=""

    def __init__(self, EID):
        self.EID = EID

    def get_bot_first_contact(self):
        first_contact_request = ei_pb2.EggIncFirstContactRequest()
        first_contact_request.ei_user_id = self.EID
        first_contact_request.client_version = 36

        url = 'https://www.auxbrain.com/ei/bot_first_contact'
        data = { 'data' : base64.b64encode(first_contact_request.SerializeToString()).decode('utf-8') }

        try:
            response = requests.post(url, data = data)

            first_contact_response = ei_pb2.EggIncFirstContactResponse()
            first_contact_response.ParseFromString(base64.b64decode(response.text))
            return {"success":True,"response":first_contact_response}
        except:
            return {"success":False,"response":None}


    def get_loot(self,ship_ID):
        loot_request=ei_pb2.MissionRequest()
        loot_request.info.identifier=ship_ID
        loot_request.ei_user_id=self.EID
        url = 'https://www.auxbrain.com/ei_afx/complete_mission'
        data = {'data': base64.b64encode(loot_request.SerializeToString()).decode('utf-8')}

        try:
            response = requests.post(url, data=data)


            aut = ei_pb2.AuthenticatedMessage()
            aut.ParseFromString(base64.b64decode(response.text))

            loot_response = ei_pb2.CompleteMissionResponse()
            loot_response.ParseFromString(aut.message)
            return loot_response
        except:
            return False
