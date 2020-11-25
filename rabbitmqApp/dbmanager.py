#from sqlalchemy import create_engine, Column, Integer, String, DateTime
#from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from models import Base, Comment
#from config import DATABASE_CONNECTION_URI

'''
#Connect to a specific database
engine = create_engine(DATABASE_CONNECTION_URI, echo = True)

# From the base, create all the tables in Base to the connected DB
Base.metadata.create_all(bind=engine)

#Create a session factory
Session = sessionmaker(bind=engine)

session = Session()'''

#Virker
def get_all_comments(session):
    #session = Session()
    comments = session.query(Comment).all()
    return comments

#virker
def request_comment(session, uId):
    #session = Session()
    #comment = session.filter_by(id=id).first()
    comment = session.query(Comment).get(uId)
    return comment
  
#Virker
def create_comment(session, authorId, postId, content):
    #session = Session()
    comment = Comment()
    comment.authorId = authorId
    comment.postId = postId
    comment.postedAt = datetime.now().isoformat()
    comment.content = content
    session.add(comment)
    session.commit()
    session.refresh(comment)
    return True
    # comment.id kan bruges til at returne actual id
    # returns commentId, postId, comment-content
    
def update_comment(session, uId, newContent):
    comment = session.query(Comment).get(uId)
    comment.content = newContent
    session.commit()
        
def delete_comment(session, uId):
    #apparently it has to be done in two steps. Can't just call .delete()
    comment = session.query(Comment).get(uId)
    session.delete(comment)
    session.commit()
    return True
    
def request_comments_for_post(session, pId):
    #session = Session()
    comments = session.query(Comment).filter(Comment.postId==pId).all()
    return comments
    





'''
create_comment(321, 123, "hello")

comments = session.query(Comment).all()
#comments = request_comments_for_post(34)

for comment in comments:
    print(comment.id)
    print(comment.postId)
    print(comment.content)


for comment in comments:
    print(comment.id)
    print(comment.content)

comments = session.query(Comment).all()

for comment in comments:
    print(comment.id)



comment = Comment()
comment.id = 999
comment.authorId = 12
comment.postId = 154
comment.postedAt = 1032
comment.content = "Hey"
session.add(comment)
session.commit()


session.close()
'''









