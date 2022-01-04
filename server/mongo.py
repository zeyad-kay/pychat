'''
Setup MongoDB schemas and provide operations for saving chats, creating and 
deleting security tokens.
chat.schema = {
    _id,
    timestamp,
    email,
    chat,
}
token.schema = {
    _id,
    timestamp,
    email,
    token,
}
'''

def connect():
    import pymongo
    import os

    CONNECTION_STRING = os.environ.get("MONGO_URI")

    return pymongo.MongoClient(CONNECTION_STRING)['pychat']
