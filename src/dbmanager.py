from datetime import datetime
from models import Base, Comment
import json
import sys
import sqlalchemy
from config import DATABASE_CONNECTION_URI
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

user_role_range = [x for x in range(10)]
mod_role_range = [x for x in range(10,20)]
admin_role_range = [x for x in range(20,30)]

def connect_db():
    engine = create_engine(DATABASE_CONNECTION_URI) #Connect to a specific database, remove echo later
    Base.metadata.create_all(bind=engine) # From the base, create all the tables in Base to the connected DB
    Session = sessionmaker(bind=engine) #Create a session factory
    session = Session() #Start a session with the engine
    return session

'''
For testing. Given a session, returns all objects for that session.

def get_all_comments():
    #session = Session()
    session = connect_db()
    comments = session.query(Comment).all()
    return comments

def remove_all_comments(properties):
    comments = get_all_comments(session)
    for comment in comments:
        delete_comment(session, comment.authorId, comment.id, 25, properties)

def size_of_db():
    size = 0
    comments = session.query(Comment).all()
    for comment in comments:
        size = size + 1
    return size
'''

def get_all_comments():
    #session = Session()
    session = connect_db()
    comments = session.query(Comment).all()
    return comments

'''
@Input - A session, and comment Id(cId)
@Output - Json object containing the comment's id, post id, 
ISO8601 timestamp(when it was created), and the content.
'''
def request_comment(cId, properties):
    print("Requesting a comment")
    try:
        session = connect_db()
        comment = session.query(Comment).get(cId)
        return json.dumps({'comment_id': comment.id, 'author_id': comment.authorId, 'post_id': comment.postId, 'created_at': comment.postedAt, 'content': comment.content, 'http_response': 200}, indent=2, default=str)
    except (sqlalchemy.exc.InterfaceError, sqlalchemy.exc.OperationalError, ConnectionRefusedError):
        print("Database is down, crashing service. Restarting, sending default error on rapid")
        jsonObject = json.dumps({'comment_id': 9999999, 'http_response': 403, 'created_at': 9999999}, indent=2, default=str)
        properties.headers['http_response'] = 503
        send("ConfirmCommentCreation", jsonObject, properties)
        raise Exception("Database is down, crashing service. Restarting, sending default error on rapid")
    except Exception as e:
        print("[-] Exception ", e.__class__, " occurred.")
        return json.dumps({'comment_id': 9999999, 'http_response': 403, 'created_at': 9999999}, indent=2, default=str)

'''
@Input - A session, authorId, postId, content
@Output - The created comment's id, ISO8601 timestamp for when it was created, 
and http response code.
'''
def create_comment(authorId, postId, content, properties):
    print("Creating a comment")
    try:
        session = connect_db()
        comment = Comment()
        comment.authorId = authorId
        comment.postId = postId
        comment.postedAt = datetime.now().isoformat()
        comment.content = content
        session.add(comment)
        session.commit()
        session.refresh(comment) # Needs this to refer to comment.id
        return json.dumps({'comment_id': comment.id, 'http_response': 200, 'created_at': comment.postedAt}, indent=2, default=str)
    except (sqlalchemy.exc.InterfaceError, sqlalchemy.exc.OperationalError, ConnectionRefusedError):
        print("Database is down, crashing service. Restarting, sending default error on rapid")
        jsonObject = json.dumps({'comment_id': 9999999, 'http_response': 403, 'created_at': 9999999}, indent=2, default=str)
        properties.headers['http_response'] = 503
        send("ConfirmCommentCreation", jsonObject, properties)
        raise Exception("Database is down, crashing service. Restarting, sending default error on rapid")
    except Exception as e:
        print("[-] Exception ", e.__class__, " occurred.")
        return json.dumps({'comment_id': 9999999, 'http_response': 403, 'created_at': 9999999}, indent=2, default=str)

'''
@Input - A session, id of the comment user wants to change,
id of the author/user wanting to make a change,
and the new content.
@Return - id of the comment being changed, http response code, 
ISO8601 timestamp representing when it was modified.
'''
def update_comment(cId, aId, newContent, role, properties):
    print("Updating a comment")
    try:
        session = connect_db()
        comment = session.query(Comment).get(cId) # Might not exist
        if(aId == comment.authorId or role in mod_role_range or role in admin_role_range):
            comment.content = newContent
            comment.postedAt = datetime.now().isoformat()
            session.commit()
            return json.dumps({'http_response': 200, 'comment_id': comment.id, 'update_timestamp': comment.postedAt}, indent=2, default=str)
        else:
            return json.dumps({'http_response': 403, 'comment_id': comment.id, 'update_timestamp': comment.postedAt}, indent=2, default=str)
    except (sqlalchemy.exc.InterfaceError, sqlalchemy.exc.OperationalError, ConnectionRefusedError):
        print("Database is down, crashing service. Restarting, sending default error on rapid")
        jsonObject = json.dumps({'http_response': 503, 'comment_id': 9999999, 'update_timestamp': 9999999}, indent=2, default=str)
        properties.headers['http_response'] = 503
        send("ConfirmCommentCreation", jsonObject, properties)
        raise Exception("Database is down, crashing service. Restarting, sending default error on rapid")
    except Exception as e:
        print("[-] Exception ", e.__class__, " occurred.")
        return json.dumps({'http_response': 503, 'comment_id': 9999999, 'update_timestamp': 9999999}, indent=2, default=str)
        
'''
@Input - A session, id of the user/author wanting to delete comment,
and the id of the comment
@Output - Http response code
'''
def delete_comment(aId, cId, role, properties):
    print("Deleting a comment")
    #apparently it has to be done in two steps. Can't just call .delete()
    try:
        session = connect_db()
        comment = session.query(Comment).get(cId) # Might not exist
        if(aId == comment.authorId or role in mod_role_range or role in admin_role_range):
            session.delete(comment)
            session.commit()
            return json.dumps({'http_response': 200}, indent=2, default=str)
        else:
            return json.dumps({'http_response': 403}, indent=2, default=str)
    except (sqlalchemy.exc.InterfaceError, sqlalchemy.exc.OperationalError, ConnectionRefusedError):
        print("Database is down, crashing service. Restarting, sending default error on rapid")
        jsonObject = json.dumps({'http_response': 503}, indent=2, default=str)
        properties.headers['http_response'] = 503
        send("ConfirmCommentCreation", jsonObject, properties)
        raise Exception("Database is down, crashing service. Restarting, sending default error on rapid")
    except Exception as e:
        print("[-] Exception ", e.__class__, " occurred.")
        return json.dumps({'http_response': 403}, indent=2, default=str)

    
'''
@Input - A session, and the id of a post
@Output - A list of comments in json format
'''
def request_comments_for_post(pId, properties):
    print("Getting comments for post")
    try:
        session = connect_db()
        comments = session.query(Comment).filter(Comment.postId==pId).all()
        jsonComments = []
        for comment in comments:
            jsonDump = json.dumps({'comment_id': comment.id, 'author_id': comment.authorId, 'post_id': comment.postId, 'created_at': comment.postedAt, 'content': comment.content}, indent=2, default=str)
            jsonComments.append(json.loads(jsonDump))
        return json.dumps({'list_of_comments': jsonComments}, indent=2, default=str)
    except (sqlalchemy.exc.InterfaceError, sqlalchemy.exc.OperationalError, ConnectionRefusedError):
        print("Database is down, crashing service. Restarting, sending default error on rapid")
        jsonObject = json.dumps({'list_of_comments': jsonComments}, indent=2, default=str)
        properties.headers['http_response'] = 503
        send("ConfirmCommentCreation", jsonObject, properties)
        raise Exception("Database is down, crashing service. Restarting, sending default error on rapid")
    except Exception as e:
        print("[-] Exception ", e.__class__, " occurred.")
        properties.headers['http_response'] = 403
        return json.dumps({'list_of_comments': jsonComments}, indent=2, default=str)