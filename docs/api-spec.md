# API Specification
For every event, if it is a request it is stated what routing key the rabbitmq message should contain. And for the response, it is stated what routing key the response to the event will be put. 
## CreateComment
Request
Routing Key - "CreateComment"
```json
{
    "user_id": "<User id of the person wanting to create a comment>",
    "post_id": "<Id of the post user wants to comment on>",
    "content": "<Content of the comment>"
}
```

Response
Routing Key - "ConfirmCommentCreation"
```json
{
    "comment_id": "<Id of the created comment>",
    "http_response": "HTTP response, 200 success, 403 unsuccessful",
    "created_at": "<ISO8601 timestamp>"
}
```

## UpdateComment
At this time, updating comments will simply replace the current content of a comment within the DB with some new content.

Request
Routing Key - "UpdateComment"
```json
{
    "comment_id": "<Id of the comment requestet>",
    "user_id": "<id of the user wanting to change a comment>",
    "content": "<Content of the new comment>"
}
```

Response
Routing Key - "ConfirmCommentUpdate"
```json
{
    "http_response": "HTTP response, 200 for success, 403 if unsuccessful",
    "comment_id": "<Id of the comment user wants to change>",
    "update_timestamp": "<ISO8601 timestamp, 1000001 if unsuccessful>"
}
```

## DeleteComment
Request
Routing Key - "DeleteComment"
```json
{
    "comment_id": "<Id of the comment user wants to delete>",
    "user_id": "<Id of the user wanting to make the change>",
}
```

Response
Routing Key - "ConfirmCommentDelete"
```json
{
    "http_response": "HTTP response, 200 for success, 403 if unsuccessful"
}
```

## RequestComment
Request
Routing Key - "RequestComment"
```json
{
    "comment_id": "<Id of the comment user wants to receive>"
}
```

Response
Routing Key - "ReturnComment"
```json
{
    "comment_id": "<Id of the comment>",
    "author_id": "<Id of the author of comment",
    "post_id": "<Id of the post associated with comment>",
    "created_at": "<ISO8601 timestamp>",
    "content": "<content>",
    "http_response": "HTTP response code, 200 for success, 403 if unsucessful"
}
```

## RequestCommentsForPost
Request
Routing Key - "RequestCommentsForPost"
```json
{
    "post_id": "<Id of the post user wants to receive comments from>"
}
```

Response
Routing Key - "ReturnCommentsForPost"
```json
{
    "list_of_comments": "<Array of comments, each element contains comments id, post id, creation time, and content.>"
}
```
