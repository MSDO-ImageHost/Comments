from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from dbmanager import get_all_comments, request_comment, update_comment, delete_comment, request_comments_for_post, create_comment
from config import DATABASE_CONNECTION_URI
from models import Base, Comment
import json
import pika
import sys

# For the db part
engine = create_engine(DATABASE_CONNECTION_URI, echo = True) #Connect to a specific database, remove echo later
Base.metadata.create_all(bind=engine) # From the base, create all the tables in Base to the connected DB
Session = sessionmaker(bind=engine) #Create a session factory
session = Session() #Start a session with the engine
# end of db part

events = ['CreateComment', 'UpdateComment', 'DeleteComment', 'RequestComment', 'RequestCommentsForPost']

def send(event, data):
    channel.basic_publish(exchange='rapid', routing_key=event, body=data)

'''
@Input: event, json data(dict)
@Output: Nothing, sends a json object onto rapid
'''
def receive(event, data):
    data = json.loads(data)
    print(data)
    print(type(data))
    if event == "CreateComment":
        jsonObject = create_comment(session, data['user-id'], data['post-id'], data['content'])
        #send(event, jsonObject)
    elif event == "UpdateComment":
        jsonObject = update_comment(session, data['comment-id'], data['user-id'], data['content'])
        #send(event, jsonObject)
    elif event == "DeleteComment":
        jsonObject = delete_comment(session, data['user-id'], data['comment-id'])
        send(event, jsonObject)
    elif event == "RequestComment":
        jsonObject = request_comment(session, data['comment-id'])
        send(event, jsonObject)
    elif event == "RequestCommentsForPost":
        jsonObject = request_comments_for_post(session, data['post-id'])
        send(event, jsonObject)

def callback(channel, method, properties, body):
    event = method.routing_key
    print(method)
    print(properties)
    print(body)
    print(receive(event, body))


connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()
channel.exchange_declare(exchange='rapid', exchange_type='direct')
channel.queue_declare('comments')

for event in events:
    channel.queue_bind(queue='comments', exchange='rapid', routing_key=event)
    
channel.basic_consume(queue='comments', on_message_callback=callback, auto_ack=True)
channel.start_consuming()



# Test stuff
'''
comments = get_all_comments(session)
for comment in comments:
    print(comment.id)
    print(comment.authorId)
    print(comment.postId)
    print(comment.content)

'''



'''

#jsonob = json.dumps({'user-id': 3, 'post-id': 5, 'content': "dajiidj"}, indent=2, default=str)
#event = "CreateComment"

#jsonob = json.dumps({'comment-id': 5, 'user-id': 3, 'content': "33333333332"}, indent=2, default=str)
#event = "UpdateComment"
#receive(event, jsonob)
#session, cId, aId, newContent
comments = get_all_comments(session)
for comment in comments:
    print(comment.id)
    print(comment.authorId)
    print(comment.postId)
    print(comment.content)




x = request_comments_for_post(session, 12)
print(x)

comments = get_all_comments(session)
for comment in comments:
    print(comment.id)
    print(comment.authorId)
    print(comment.postId)
    print(comment.content)
'''

