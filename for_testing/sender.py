## ONLY a tester file..

import pika, json

connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()
channel.exchange_declare(exchange='rapid', exchange_type='direct')

jsonob = json.dumps({'user-id': 333, 'post-id': 555, 'content': "herro my man"}, indent=2, default=str)
#jsonob = json.dumps({'comment-id': 0}, indent=2, default=str)
event = "CreateComment"

channel.basic_publish(exchange='rapid', routing_key=event, body=jsonob)
connection.close()