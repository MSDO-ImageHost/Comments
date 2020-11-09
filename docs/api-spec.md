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
    "commentID": "<comment-id>"
}
```

## UpdateComment
Request
```json
{
    "comment-identifier": "<comment-id>",
    "new-content": "<content>"
}
```

Response
```json
{
    "confirm-update": "<Boolean>",
    "commentID": "<comment-id>"
}
```

## DeleteComment
Request
```json
{
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
