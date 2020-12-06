from datetime import datetime
from models import Base, Comment
import json

'''
For testing. Given a session, returns all objects for that session.
'''
def get_all_comments(session):
    #session = Session()
    comments = session.query(Comment).all()
    return comments

def remove_all_comments(session):
    comments = get_all_comments(session)
    for comment in comments:
        delete_comment(session, comment.authorId, comment.id)

'''
For testing
'''
def size_of_db(session):
    size = 0
    comments = session.query(Comment).all()
    for comment in comments:
        size = size + 1
    return size

'''
@Input - A session, and comment Id(cId)
@Output - Json object containing the comment's id, post id, 
ISO8601 timestamp(when it was created), and the content.
'''
def request_comment(session, cId):
    try:
        comment = session.query(Comment).get(cId)
        return json.dumps({'comment-id': comment.id, 'post-id': comment.postId, 'created-at': comment.postedAt, 'content': comment.content, 'http-response': 200}, indent=2, default=str)
    except:
        return json.dumps({'comment-id': cId, 'post-id': 999999, 'created-at': 999999, 'content': "Could not find comment", 'http-response': 403}, indent=2, default=str)
'''
@Input - A session, authorId, postId, content
@Output - The created comment's id, ISO8601 timestamp for when it was created, 
and http response code.
'''
def create_comment(session, authorId, postId, content):
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
    try:
        comment = session.query(Comment).get(cId) # Might not exist
        if(aId == comment.authorId):
            comment.content = newContent
            comment.postedAt = datetime.now().isoformat()
            session.commit()
            return json.dumps({'http-response': 200, 'comment-id': comment.id, 'update-timestamp': comment.postedAt}, indent=2, default=str)
        else:
            return json.dumps({'http-response': 403, 'comment-id': comment.id, 'update-timestamp': comment.postedAt}, indent=2, default=str)
    except:
        return json.dumps({'http-response': 403, 'comment-id': cId, 'update-timestamp': 1000001}, indent=2, default=str)
        
'''
@Input - A session, id of the user/author wanting to delete comment,
and the id of the comment
@Output - Http response code
'''
def delete_comment(session, aId, cId):
    #apparently it has to be done in two steps. Can't just call .delete()
    try:
        comment = session.query(Comment).get(cId) # Might not exist
        if(aId == comment.authorId):
            session.delete(comment)
            session.commit()
            return json.dumps({'http-response': 200}, indent=2, default=str)
        else:
            return json.dumps({'http-response': 403}, indent=2, default=str)
    except:
        return json.dumps({'http-response': 403}, indent=2, default=str)

    
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