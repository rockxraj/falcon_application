import falcon
import json
import requests
import sys
import datetime

from peewee import *

db = SqliteDatabase('chatBot.db')

class Chat(Model):
    msg = CharField(max_length=255)
    class Meta:
        database = db # This model uses the "people.db" database.

if __name__ == '__main__':
    db.connect()
    db.create_tables([Chat])

class TestResource(object):
    def on_get(self, req, res):
        """Handles all GET requests."""
        res.status = falcon.HTTP_200  # This is the default status
        result =  Chat.select().get().msg
        su ='https://webchat.botframework.com/v3/directline/conversations/ea3488d41ce748c796546941e939dd0a/activities'
        cl = "1509614258436.0034845801641907315.2"
        repl = 'Bot26111991'
        rec = {"id":"7Y3ea3488d41ce748c796546941e939dd0aTok4tIsY", "name": "Rockxraj"}
        fr = {"id": "28197c53-926e-45a5-ad43-cc47ff011670"}
        msgd = 'hello! Raj'
        msgTy = 'message'
        con = {"id":"ea3488d41ce748c796546941e939dd0a",  "name": "conversation's name"}
        result1 = sendMessage(su, cl, repl, fr, rec, msgd, msgTy, con)
        res.body = result1
        
    def on_post(self, req, res):
        res.status = falcon.HTTP_200
        data = req.stream.read()
        msgdata = Chat(msg=data)
        msgdata.save()
        res.body = 'successfully sent'
        

app_client_id = '28197c53-926e-45a5-ad43-cc47ff011670'
app_client_secret = 'toyvtGREIN41!xbBC440)%@'

def sendMessage(serviceUrl,channelId,replyToId,fromData, recipientData,message,messageType,conversation):
    url="https://login.microsoftonline.com/common/oauth2/v2.0/token"
    data = {"grant_type":"client_credentials",
        "client_id":app_client_id,
        "client_secret":app_client_secret,
        "scope":"https://graph.microsoft.com/.default"
       }
    response = requests.post(url,data)
    resData = response.json()
    responseURL = serviceUrl + "v3/conversations/%s/activities/%s" % (conversation["id"],replyToId)
    chatresponse = requests.post(
                       responseURL,
                       json={
                        "type": messageType,
                        "timestamp": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f%zZ"),
                        "from": fromData,
                        "conversation": conversation,
                        "recipient": recipientData,
                        "text": message,
                        "replyToId": replyToId
                       },
                       headers={
                           "Authorization":"%s %s" % (resData["token_type"],resData["access_token"])
                       }
                    )
# Create the Falcon application object
app = falcon.API()

# Instantiate the TestResource class
test_resource = TestResource()

# Add a route to serve the resource
app.add_route('/test', test_resource)
