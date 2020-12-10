## ONLY a tester file..

import pika, json
from config import AMQP_PASSWORD, AMQP_USER

credentials = pika.PlainCredentials(AMQP_USER, AMQP_PASSWORD)
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='rabbitmq',
    port=5672,
    virtual_host='/',
    credentials=credentials))
channel = connection.channel()
channel = connection.channel()
channel.exchange_declare(exchange='rapid', exchange_type='direct')

jsonob = json.dumps({'user_id': 3, 'post_id': 5, 'content': "kms"}, indent=2, default=str)
event = "CreateComment"
hdrs = {'jwt': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxIiwicm9sZSI6MSwiaXNzIjoiSW1hZ2VIb3N0LnNkdS5kayIsImV4cCI6MTYwODUyMDMyOSwiaWF0IjoxNjA3MjA2MzI5fQ.EFv8rHJYAp0DE8h2GFzZzceCiOZS4ZfCh6aBkIHNsEs', 'http-response': '200'}

properties = pika.BasicProperties(correlation_id='1337',
    content_type='application/json',  
    headers=hdrs)

channel.basic_publish(exchange='rapid',
                        routing_key=event, 
                        body=jsonob, 
                        properties=properties)
connection.close()

