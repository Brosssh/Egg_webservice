import hashlib
from google.protobuf.json_format import MessageToDict, MessageToJson


def encrypt_string(hash_string):
    sha_signature = hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature

def protoToJson(proto_message):
    return MessageToJson(proto_message)

def protoToDict(proto_message):
    return MessageToDict(proto_message)