# API Specification

## CreateComment
Request
```json
{
    "comment-creator": "<user-id>",
    "post-id": "<post-id>",
    "comment-content": "<content>"
}
```

Response
```json
{
    "comment-id": "<comment-id>",
    "http-response": "HTTP response",
    "created-at": "<ISO8601 timestamp>"
}
```

## UpdateComment
At this time, updating comments will simply replace the current content of a comment within the DB with some new content.

Request
```json
{
    "comment-updater": "<user-id>",
    "comment-identifier": "<comment-id>",
    "new-content": "<content>"
}
```

Response
```json
{
    "http-response": "HTTP response",
    "comment-id": "<comment-id>",
    "update-timestamp": "<ISO8601 timestamp>"
}
```

## DeleteComment
Request
```json
{
    "comment-deletor": "<user-id>",
    "comment-identifier": "<comment-id>"
}
```

Response
```json
{
    "http-response": "HTTP response"
}
```

## RequestComment
Request
```json
{
    "commentID": "<comment-id>"
}
```

Response
```json
{
    "comment-id": "<commend-id>",
    "post-id": "<post-id>",
    "created-at": "<ISO8601 timestamp>",
    "content": "<content>",
    "http-response": "HTTP response code"
}
```

## RequestCommentsForPost
Request
```json
{
    "post-identifier": "<post-id>"
}
```

Response
```json
{
    "list-of-comment-ids": "<Array>"
}
```
