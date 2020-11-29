#from sqlalchemy import create_engine, Column, Integer, String, DateTime
#from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from models import Base, Comment
import json
#from config import DATABASE_CONNECTION_URI

'''
#Connect to a specific database
engine = create_engine(DATABASE_CONNECTION_URI, echo = True)

# From the base, create all the tables in Base to the connected DB
Base.metadata.create_all(bind=engine)

#Create a session factory
Session = sessionmaker(bind=engine)

session = Session()'''

'''
For testing. Given a session, returns all objects for that session.
'''
def get_all_comments(session):
    #session = Session()
    comments = session.query(Comment).all()
    return comments

'''
@Input - A session, and comment Id(cId)
@Output - Json object containing the comment's id, post id, 
ISO8601 timestamp(when it was created), and the content.
'''
def request_comment(session, cId):
    comment = session.query(Comment).get(cId)
    return json.dumps({'comment-id': comment.id, 'post-id': comment.postId, 'created-at': comment.postedAt, 'content': comment.content}, indent=2, default=str)
  
'''
@Input - A session, authorId, postId, content
@Output - The created comment's id, ISO8601 timestamp for when it was created, 
and http response code.
'''
def create_comment(session, authorId, postId, content):
    #session = Session()
    comment = Comment()
    comment.authorId = authorId
    comment.postId = postId
    comment.postedAt = datetime.now().isoformat()
    comment.content = content
    session.add(comment)
    session.commit()
    session.refresh(comment) # Needs this to refer to comment.id
    return json.dumps({'comment-id': comment.id, 'http-response': 200, 'created-at': comment.postedAt}, indent=2, default=str)
    
'''
@Input - A session, id of the comment user wants to change,
id of the author/user wanting to make a change,
and the new content.
@Return - id of the comment being changed, http response code, 
ISO8601 timestamp representing when it was modified.
'''
def update_comment(session, cId, aId, newContent):
    comment = session.query(Comment).get(cId)
    if(aId == comment.authorId):
        comment.content = newContent
        comment.postedAt = datetime.now().isoformat()
        session.commit()
        return json.dumps({'confirm-delete': 200, 'comment-id': comment.id, 'update-timestamp': comment.postedAt}, indent=2, default=str)
    else:
        return json.dumps({'confirm-delete': 403, 'comment-id': comment.id, 'update-timestamp': comment.postedAt}, indent=2, default=str)
        
'''
@Input - A session, id of the user/author wanting to delete comment,
and the id of the comment
@Output - Http response code
'''
def delete_comment(session, aId, cId):
    #apparently it has to be done in two steps. Can't just call .delete()
    comment = session.query(Comment).get(cId)
    if(aId == comment.authorId):
        session.delete(comment)
        session.commit()
        return json.dumps({'confirm-delete': 200}, indent=2, default=str)
    else:
        return json.dumps({'confirm-delete': 403}, indent=2, default=str)

    
'''
@Input - A session, and the id of a post
@Output - A list of comment id's which is connected to that post.
'''
def request_comments_for_post(session, pId):
    comments = session.query(Comment).filter(Comment.postId==pId).all()
    commentIdArray = []
    for comment in comments:
        commentIdArray.append(comment.id)
    return json.dumps({'list-of-comment-ids': commentIdArray}, indent=2, default=str)
    