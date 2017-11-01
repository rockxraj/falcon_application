import falcon
import json

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
        res.body = result
        
    def on_post(self, req, res):
        res.status = falcon.HTTP_200
        data = req.stream.read()
        msgdata = Chat(msg=data)
        msgdata.save()
        res.body = Chat.select().get().msg 


# Create the Falcon application object
app = falcon.API()

# Instantiate the TestResource class
test_resource = TestResource()

# Add a route to serve the resource
app.add_route('/test', test_resource)
