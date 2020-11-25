from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, DateTime

# Base which is shared by "all" of the models
Base = declarative_base()

############# Models ################

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    authorId = Column(Integer)
    postId = Column(Integer)
    postedAt = Column(DateTime)
    content = Column(String(100))
