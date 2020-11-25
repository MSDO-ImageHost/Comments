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
    "commentID": "<comment-id>",
    "confirm-create": "HTTP response",
    "comment-timestamp": "<ISO8601 timestamp>"
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
    "confirm-update": "<Boolean>",
    "commentID": "<comment-id>",
    "update-timestamp": "<ISO8601 timestamp>",
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
    "confirm-delete": "<HTTP response code>"
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
    "comment-content": "<content>"
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
