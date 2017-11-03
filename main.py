import falcon
import json
import requests
import sys
from datetime import datetime

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
        res.status = falcon.HTTP_200 
        #result =  Chat.select().get().msg
        recieveFromBot()
        res.body = "sucessfully get"
        
    def on_post(self, req, res) :
        res.status = falcon.HTTP_200
        data = req.stream.read() 
        sendToBot()
        res.body = "successfully sent message"

app_client_id = '28197c53-926e-45a5-ad43-cc47ff011670'
app_client_secret = 'toyvtGREIN41!xbBC440)%@'

def getData(tokenResponseData):
    #print 'under getdata()\n\n'
    #serviceUrl = "https://directline.botframework.com/"  
    serviceUrl = "https://webchat.botframework.com/"  
    tokenPayload ={ "Authorization": "Bearer %s" % tokenResponseData["token"]}
    requestURL = serviceUrl + "v3/directline/conversations/%s/activities" % (tokenResponseData["conversationId"])
    #print requestURL
    botResponse =requests.get(requestURL,headers = tokenPayload)
    #print botResponse.json()    

def recieveFromBot():
    #serviceUrl = "https://directline.botframework.com/"
    serviceUrl = "https://webchat.botframework.com/"
    url = "https://directline.botframework.com/v3/directline/conversations"
    payload = { "Authorization" : "Bearer gvTJg8q_2rY.cwA.L6Q.08Av9U0yKi5vGZGQ8qDcqwKU2wvYyxzZHtKMlyNDgio" }
    tokenResponse = requests.post(url,headers =payload )
    tokenResponseData = tokenResponse.json()

    tokenPayload ={ "Authorization": "Bearer %s" % tokenResponseData["token"]}
    requestURL = serviceUrl + "v3/directline/conversations/%s/activities" % (tokenResponseData["conversationId"])
    
    botResponse =requests.get(requestURL,headers = tokenPayload)
    #print botResponse.json()


def sendToBot():
    #serviceUrl = "https://directline.botframework.com/"
    serviceUrl = "https://webchat.botframework.com/"
    #url = "https://directline.botframework.com/v3/directline/conversations"
    url = "https://webchat.botframework.com/v3/directline/conversations" 
    payload = { "Authorization" : "Bearer gvTJg8q_2rY.cwA.L6Q.08Av9U0yKi5vGZGQ8qDcqwKU2wvYyxzZHtKMlyNDgio" }
    tokenResponse = requests.post(url,headers =payload )
    tokenResponseData = tokenResponse.json()
    #print tokenResponseData
    #print tokenResponseData["conversationId"]
    #print "Bearer %s" % tokenResponseData["token"]
    tokenPayload ={ "Authorization": "Bearer %s" % tokenResponseData["token"]}
    #print tokenPayload
    responseURL = serviceUrl + "v3/directline/conversations/%s/activities" % (tokenResponseData["conversationId"])

    chatResponse = requests.post(responseURL,json= {
        "type": "message",
        "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f%zZ"),
        "from": { "id": "7Y3Tok4tIsY", "name": "You"},
        "text": "Hello Raj you have successfully posted data !!",
        "locale":"en-US",
        "textFormat": "plain"},
                                 headers = tokenPayload
    )                        
    #print chatResponse
   # print chatResponse.json()
    getData(tokenResponseData)


# def sendMessage(serviceUrl,channelId,replyToId,fromData, recipientData,message,messageType,conversation):
#     url="https://login.microsoftonline.com/common/oauth2/v2.0/token"
#     data = {"grant_type":"client_credentials",
#         "client_id":app_client_id,
#         "client_secret":app_client_secret,
#         "scope":"https://graph.microsoft.com/.default"
#        }
#     response = requests.post(url,data)
#     resData = response.json()
#     #responseURL = serviceUrl + "v3/conversations/%s/activities/%s" % (conversation["id"],replyToId)
#     responseURL = serviceUrl + "v3/conversations/%s/activities/" % (conversation)
#     chatresponse = requests.post(
#                        responseURL,
#                        json={
#                         "type": messageType,
#                         "timestamp": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f%zZ"),
#                         "from": fromData,
#                         "conversation": conversation,
#                         "recipient": recipientData,
#                         "text": message,
#                         "replyToId": replyToId
#                        },
#                        headers={
#                            "Authorization":"%s %s" % (resData["token_type"],resData["access_token"])
#                        }
#                     )
# Create the Falcon application object
app = falcon.API()

# Instantiate the TestResource class
test_resource = TestResource()

# Add a route to serve the resource
app.add_route('/test', test_resource)
