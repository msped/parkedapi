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
        'author': int,
        'image': file,
        'description': string,
        'comments_enabled': boolean
    }
```

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

```
    {
        'profile': int
    }
```

### Like Comment

```/api/posts/comment/like/:slug POST```

```
    {
        'profile': int
    }
```
