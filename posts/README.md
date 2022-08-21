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

```/api/posts/comment/new POST```

```
    {
        'profile': int,
        'post': int
    }
```

### Like Post

```/api/posts/like/:slug POST```

### Like Comment

```/api/posts/comment/like/:slug POST```
