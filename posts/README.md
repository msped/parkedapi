# Posts 

## Endpoints

The layout for each each point is 

```URL METHOD```

```
{ 
    POST Dict 
}
```

### New Post

```/api/posts/new/ POST```

```
    {
        'image': file,
        'description': string,
        'comments_enabled': boolean
    }
```

This must be sent as `format='multipart'`

### New Comment 

```/api/posts/:slug/comment/new/ POST```

```
    {
        'content': string
    }
```

### Like Post

```/api/posts/like/:slug/ POST```

### Like Comment

```/api/posts/comment/like/:id/ POST```

### Post

```/api/posts/:slug/ GET```

```/api/posts/:slug/ PATCH```

```/api/posts/:slug/ DELETE```

### Comment

```/api/posts/comment/:id/ GET```

```/api/posts/comment/:id/ PATCH```

{
    'content': string
}

```/api/posts/comment/:id/ DELETE```
