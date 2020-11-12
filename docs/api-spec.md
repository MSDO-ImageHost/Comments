# API Specification

## CreateComment
Request
```json
{
    "comment-creator": "<user-id>",
    "post-identifier": "<post-id>",
    "comment-content": "<content>"
}
```

Response
```json
{
    "confirm-create": "<Boolean>",
    "commentID": "<comment-id>",
    "comment-timestamp": "<ISO8601 timestamp>",
}
```

## UpdateComment
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
    "comment-updater": "<user-id>",
    "comment-identifier": "<comment-id>"
}
```

Response
```json
{
    "confirm-delete": "<Boolean>"
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
    "comment-content": "<content>",
    "comment-id": "<commend-id>"
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
