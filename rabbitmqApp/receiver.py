from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from dbmanager import get_all_comments, request_comment, update_comment, delete_comment, request_comments_for_post, create_comment
from config import DATABASE_CONNECTION_URI
from models import Base, Comment
import json

engine = create_engine(DATABASE_CONNECTION_URI, echo = True) #Connect to a specific database
Base.metadata.create_all(bind=engine) # From the base, create all the tables in Base to the connected DB
Session = sessionmaker(bind=engine) #Create a session factory
session = Session() #Start a session with the engine

update_comment(session, 1, 32, "fap fap fap ")


comments = get_all_comments(session)
for comment in comments:
    print(comment.id)
    print(comment.authorId)
    print(comment.content)


