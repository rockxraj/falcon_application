import falcon
import json
import requests
import sys
from datetime import datetime
from array import array

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
        #recieveFromBot()
        res.body = "sucessfully get"
        
    def on_post(self, req, res) :
        res.status = falcon.HTTP_200
        data = req.stream.read()
        print(data)
        a = json.loads(data.decode('utf-8'))
        print(a['text'])
        print(a['conversation']['id'])
        print(a['serviceUrl'])
        print(a['id'])
        sendMessage(a['serviceUrl'], a['conversation']['id'] , a['id'], "Hi Raj")
        res.body = "posted"
        

app_client_id = '28197c53-926e-45a5-ad43-cc47ff011670'
app_client_secret = 'toyvtGREIN41!xbBC440)%@'

def sendMessage( serviceUrl, conversationId, replyToId, msg):
    url="https://login.microsoftonline.com/botframework.com/oauth2/v2.0/token"
    data = {"grant_type":"client_credentials",
        "client_id":app_client_id,
        "client_secret":app_client_secret,
        #"scope":"https%3A%2F%2Fapi.botframework.com%2F.default"
        "scope" : "https://api.botframework.com/.default"
    }
    header = {"Content-Type" : "application/x-www-form-urlencoded", "Host": "login.microsoftonline.com"}
    response = requests.post(url,data, headers = header)
    resData = response.json()
    abc ={"Authorization" : "%s %s" % (resData["token_type"],resData["access_token"]), "Content-Type": "application/json"}
    
    print(resData)
    print(conversationId[3:])
    
    replyConUrl = serviceUrl + 'v3/%s/conversations/activities/%s' % (conversationId[3:], replyToId)
    print(ReplyConUrl)
    replyConversationResponse = requests.post( replyConUrl, 
                                          json = {
                                              "text": msg,
                                              "type":"message",
                                              "timestamp":datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f%zZ"),
                                              "localTimestamp":"2017-11-06T18:02:08.173+05:30",
                                              "replyToId":replyToId,
                                              "channelId":"skype",
                                              "serviceUrl":"https://smba.trafficmanager.net/apis/",
                                              "from":{"id":"29:28197c53-926e-45a5-ad43-cc47ff011670","name":"Rockxraj"},
                                              "conversation":{"id": conversationId },
                                              "recipient":{"id":"28:1tiv_UrrNJp1UKSRV0fw9V_nZhZIwbuYhnGtJBr1Lcw86LWNS4HzKHfvlCdrnqIVb","name":"Rajendra Gupta"}
                                              #"entities":[{"locale":"en-US","country":"US","platform":"Mac","type":"clientInfo"}],
                                              #"channelData":{"text": msg}
                                          },
                                          headers = abc)    
    print(replyConversationResponse)
    #print (conversationResponse.json())
    
    # conversationId = conversationResponse.json()
    # abcd ={"Authorization" : "%s %s" % (resData["token_type"],resData["access_token"]), "Content-Type": "application/json"}
    # responseUrl = serviceUrl + "/v3/conversations/%s/activities" % (conversationId["id"][3:])

    # #print responseUrl

    # chatResponse = requests.post(
    #                    responseUrl,
    #                    json =  {
    #                        "type": "message",
    #                        "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f%zZ"),
    #                        "from": {
    #                            "id": "29:28197c53-926e-45a5-ad43-cc47ff011670",
    #                            "name": "Rockxraj"
    #                        },
    #                        "conversation": {
    #                            "isGroup": "false",
    #                            "id": "28:rajendra.g@amazatic.com"
    #                        },
    #                        "recipient": {
    #                            "id": "28:rajendra.g@amazatic.com",
    #                            "name": "Rajendra Gupta"
    #                        },
    #                        "text": "Good morning !" ,
    #                        "textFormat" : "plain"
    #                    },
    #                     headers = abcd
    #                 )
    # #print chatResponse
    
# def getData(tokenResponseData):
#     #print 'under getdata()\n\n'
#     serviceUrl = "https://directline.botframework.com/"  
#     tokenPayload ={ "Authorization": "Bearer %s" % tokenResponseData["token"]}
#     requestURL = serviceUrl + "v3/directline/conversations/%s/activities" % (tokenResponseData["conversationId"])
#     #print requestURL
#     botResponse =requests.get(requestURL,headers = tokenPayload)
#     #print botResponse.json()    

# def recieveFromBot():
#     serviceUrl = "https://directline.botframework.com/"
    
#     url = "https://directline.botframework.com/v3/directline/conversations"
#     payload = { "Authorization" : "Bearer gvTJg8q_2rY.cwA.L6Q.08Av9U0yKi5vGZGQ8qDcqwKU2wvYyxzZHtKMlyNDgio" }
#     tokenResponse = requests.post(url,headers =payload )
#     tokenResponseData = tokenResponse.json()

#     tokenPayload ={ "Authorization": "Bearer %s" % tokenResponseData["token"]}
#     requestURL = serviceUrl + "v3/directline/conversations/%s/activities" % (tokenResponseData["conversationId"])
    
#     botResponse =requests.get(requestURL,headers = tokenPayload)
#     #print botResponse.json()


# def sendToBot():
#     serviceUrl = "https://directline.botframework.com/"
#     url = "https://directline.botframework.com/v3/directline/conversations"
    
#     payload = { "Authorization" : "Bearer gvTJg8q_2rY.cwA.L6Q.08Av9U0yKi5vGZGQ8qDcqwKU2wvYyxzZHtKMlyNDgio" }
#     tokenResponse = requests.post(url,headers =payload )
#     tokenResponseData = tokenResponse.json()
#     #print tokenResponseData
#     #print tokenResponseData["conversationId"]
#     #print "Bearer %s" % tokenResponseData["token"]
#     tokenPayload ={ "Authorization": "Bearer %s" % tokenResponseData["token"]}
#     #print tokenPayload
#     responseURL = serviceUrl + "v3/directline/conversations/%s/activities" % (tokenResponseData["conversationId"])

#     chatResponse = requests.post(responseURL,json= {
#         "type": "message",
#         "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f%zZ"),
#         "from": { "id": "7Y3Tok4tIsY", "name": "You"},
#         "text": "Hello Raj you have successfully posted data !!",
#         "locale":"en-US",
#         "textFormat": "plain"},
#                                  headers = tokenPayload
#     )                        
#     #print chatResponse
#     #print chatResponse.json()
#     #getData(tokenResponseData)'''



# Create the Falcon application object
app = falcon.API()

# Instantiate the TestResource class
test_resource = TestResource()

# Add a route to serve the resource
app.add_route('/test', test_resource)
