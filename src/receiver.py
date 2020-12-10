from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from dbmanager import get_all_comments, request_comment, update_comment, delete_comment, request_comments_for_post, create_comment
from config import DATABASE_CONNECTION_URI
from models import Base, Comment
from jose import jwt
import json
import pika
import sys
import time
from config import AMQP_PASSWORD, AMQP_USER, AMQP_URI

# For the db part
engine = create_engine(DATABASE_CONNECTION_URI, echo = True) #Connect to a specific database, remove echo later
Base.metadata.create_all(bind=engine) # From the base, create all the tables in Base to the connected DB
Session = sessionmaker(bind=engine) #Create a session factory
session = Session() #Start a session with the engine
# end of db part

events = ['CreateComment', 'UpdateComment', 'DeleteComment', 'RequestComment', 'RequestCommentsForPost']

'''
@Input: Event string, json data(dict)
@Output: None, puts object onto rapid
'''
def send(event, data, properties):
    channel.basic_publish(exchange='rapid', routing_key=event, body=data, properties=properties)

#It decodes the token and makes sure that the issuer is what we expect and that it has not expired
def verify(token):
    try:
        decoded = jwt.decode(token, "secret", algorithms=['HS256'])
        millis = int(round(time.time() * 1000))
        if (decoded["iss"] == "ImageHost.sdu.dk" and decoded["exp"] < millis):
            return decoded
        else:
            return None
    except:
        return None

'''
@Input: event string, json data(dict)
@Output: Nothing, calls a function to put object onto rapid
'''
def receive(event, data, properties):
    data = json.loads(data)
    jwt = verify(properties.headers['jwt'])
    user_id = jwt['sub']
    role = jwt['role']

    if(jwt):
        if event == "CreateComment":
            jsonObject = create_comment(session, user_id, data['post_id'], data['content'])
            # Get the actual http response from the action and put it into properties
            httpResponse = json.loads(jsonObject)['http_response']
            properties.headers['http_response'] = httpResponse
            send("ConfirmCommentCreation", jsonObject, properties)
        elif event == "UpdateComment":
            jsonObject = update_comment(session, data['comment_id'], user_id, data['content'], role)
            httpResponse = json.loads(jsonObject)['http_response']
            properties.headers['http_response'] = httpResponse
            send("ConfirmCommentUpdate", jsonObject, properties)
        elif event == "DeleteComment":
            jsonObject = delete_comment(session, user_id, data['comment_id'], role)
            httpResponse = json.loads(jsonObject)['http_response']
            properties.headers['http_response'] = httpResponse
            send("ConfirmCommentDelete", jsonObject, properties)
        elif event == "RequestComment":
            jsonObject = request_comment(session, data['comment_id'])
            httpResponse = json.loads(jsonObject)['http_response']
            properties.headers['http_response'] = httpResponse
            send("ReturnComment", jsonObject, properties)
        elif event == "RequestCommentsForPost":
            jsonObject = request_comments_for_post(session, data['post_id'])
            send("ReturnCommentsForPost", jsonObject, properties)
        else:
            pass
    else:
        # What should happen if an invalid jwt was given?
        pass

def callback(channel, method, properties, body):
    event = method.routing_key
    print("###################################")
    print(method)
    print(properties)
    print("Imma kms")
    print(verify(properties.headers['jwt']))
    print(body)
    print("###################################")
    receive(event, body, properties)

if __name__ == '__main__':
    
    comments = get_all_comments(session)
    for comment in comments:
        print(comment.id)
        print(comment.authorId)
        print(comment.postId)
        print(comment.content)
    '''

    credentials = pika.PlainCredentials(AMQP_USER, AMQP_PASSWORD)
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='rabbitmq',
        port=5672,
        virtual_host='/',
        credentials=credentials))
    channel = connection.channel()
    channel.exchange_declare(exchange='rapid', exchange_type='direct')
    channel.queue_declare('comments')

    for event in events:
        channel.queue_bind(queue='comments', exchange='rapid', routing_key=event)
        
    channel.basic_consume(queue='comments', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()'''