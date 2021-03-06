from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from dbmanager import get_all_comments, request_comment, update_comment, delete_comment, request_comments_for_post, create_comment, delete_comments_for_post
from config import DATABASE_CONNECTION_URI
from models import Base, Comment
from jose import jwt
import mysql.connector
import json
import pika
import sys
import time
from config import AMQP_PASSWORD, AMQP_USER, AMQP_URI, RABBITMQ_PORT, RABBITMQ_HOST

# For the db part
print("Connecting to database")
engine = create_engine(DATABASE_CONNECTION_URI) #Connect to a specific database, remove echo later
Base.metadata.create_all(bind=engine) # From the base, create all the tables in Base to the connected DB
Session = sessionmaker(bind=engine) #Create a session factory
session = Session() #Start a session with the engine
print("Succesfully connected to database")
# end of db part

events = ['CreateComment', 'UpdateComment', 'DeleteComment', 'RequestComment', 'RequestCommentsForPost', "ConfirmOnePostDeletion"]

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
    print(properties.headers)
    jwt = verify(properties.headers['jwt'])

    if event == "CreateComment":
        if(jwt):
            jsonObject = create_comment(session, int(jwt['sub']), data['post_id'], data['content'], properties)
            # Get the actual http response from the action and put it into properties
            httpResponse = json.loads(jsonObject)['http_response']
            properties.headers['http_response'] = httpResponse
            send("ConfirmCommentCreation", jsonObject, properties)
            print(f'Created comment with json: {jsonObject}')
        else:
            errorJson = json.dumps({'comment_id': 2147483645, 'http_response': 403, 'created_at': 1000001}, indent=2, default=str)
            send("ConfirmCommentCreation", errorJson, properties)
            print(f'Created comment with json: {jsonObject}')

    elif event == "UpdateComment":
        if(jwt):
            jsonObject = update_comment(session, int(data['comment_id']), int(jwt['sub']), data['content'], int(jwt['role']), properties)
            httpResponse = json.loads(jsonObject)['http_response']
            properties.headers['http_response'] = httpResponse
            send("ConfirmCommentUpdate", jsonObject, properties)
            print(f'Updated comment with {jsonObject}')
        else:
            errorJson = json.dumps({'http_response': 403, 'comment_id': data['comment_id'], 'update_timestamp': 1000001}, indent=2, default=str)
            send("ConfirmCommentUpdate", errorJson, properties)
            print(f'Updated comment with {jsonObject}')

    elif event == "DeleteComment":
        if(jwt):
            jsonObject = delete_comment(session, int(jwt['sub']), int(data['comment_id']), int(jwt['role']), properties)
            httpResponse = json.loads(jsonObject)['http_response']
            properties.headers['http_response'] = httpResponse
            send("ConfirmCommentDelete", jsonObject, properties)
            print(f'Deleted comment with {jsonObject}')
        else:
            errorJson = json.dumps({'http_response': 403}, indent=2, default=str)
            send("ConfirmCommentDelete", errorJson, properties)
            print(f'Deleted comment with {jsonObject}')

    elif event == "ConfirmOnePostDeletion":
        # No checking needed, as this has been done by the one triggering the event
        delete_comments_for_post(session, data['post_id']) 
        

    elif event == "RequestComment":
        jsonObject = request_comment(session, data['comment_id'], properties)
        httpResponse = json.loads(jsonObject)['http_response']
        properties.headers['http_response'] = httpResponse
        send("ReturnComment", jsonObject, properties)
        print(f'Requested comment with {jsonObject}')

    elif event == "RequestCommentsForPost":
        jsonObject = request_comments_for_post(session, data['post_id'], properties)
        properties.headers['http_response'] = 200
        send("ReturnCommentsForPost", jsonObject, properties)
        print(f'Requested comment for post {jsonObject}')

    else:
        pass # A wrong event has been given    

def callback(channel, method, properties, body):
    event = method.routing_key
    print("###################################")
    print(method)
    print(properties)
    print(body)
    print("###################################")
    receive(event, body, properties)

if __name__ == '__main__':
    print("Trying to connect to rabbitmq")
    print("Rabbit host:", RABBITMQ_HOST)
    print("Rabbit user:", AMQP_USER)
    print("Rabbit pass:", AMQP_PASSWORD)
    credentials = pika.PlainCredentials(AMQP_USER, AMQP_PASSWORD)
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        virtual_host='/',
        credentials=credentials))
    channel = connection.channel()
    channel.exchange_declare(exchange='rapid', exchange_type='direct')
    channel.queue_declare('comments')
    print("Succesfully connected to rabbitmq")

    for event in events:
        print(f"Binding to event: {event}")
        channel.queue_bind(queue='comments', exchange='rapid', routing_key=event)
    print("Starts consuming:")
    channel.basic_consume(queue='comments', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()
