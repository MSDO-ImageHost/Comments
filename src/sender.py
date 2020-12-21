## ONLY a tester file..

import pika, json
from config import AMQP_PASSWORD, AMQP_USER
from dbmanager import get_all_comments, request_comments_for_post, request_comment

credentials = pika.PlainCredentials(AMQP_USER, AMQP_PASSWORD)
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='rabbitmq',
    port=5672,
    virtual_host='/',
    credentials=credentials))
channel = connection.channel()
channel = connection.channel()
channel.exchange_declare(exchange='rapid', exchange_type='direct')


# Create a comment:
jsonob = json.dumps({'user_id': "3", 'post_id': "5", 'content': "imma fking yeet"}, indent=2, default=str)
event = "CreateComment"

# Update a comment:
#jsonob = json.dumps({'comment_id': 16, 'user_id': 1, 'content': "I am changed, still yeeting"}, indent=2, default=str)
#event = "UpdateComment"

# Delete a comment:
#jsonob = json.dumps({'user_id': 1, 'comment_id': 16}, indent=2, default=str)
#event = "DeleteComment"


hdrs = {'jwt': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI1Iiwicm9sZSI6MCwiaXNzIjoiSW1hZ2VIb3N0LnNkdS5kayIsImV4cCI6MTYzODU2MDcxMywiaWF0IjoxNjA3MDI0NzEzfQ.BEd5MV1_8Vukwk-zX3cNKrXKF_ZseIBmahYt7-PopB8', 'http_response': '200'}

properties = pika.BasicProperties(correlation_id='1337',
    content_type='application/json',  
    headers=hdrs)

channel.basic_publish(exchange='rapid',
                        routing_key=event, 
                        body=jsonob, 
                        properties=properties)
connection.close()

comments = get_all_comments()
for comment in comments:
    print(comment.id)
    print(comment.authorId)
    print(comment.postId)
    print(comment.content)

