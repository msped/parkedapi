# Profile Auth App

## Endpoints

The layout for each each point is 

```URL METHOD```

```
{ 
    POST Dict 
}
```

Further Information

----------------------------

### Obtain Token (Login)

```/api/auth/jwt/create/ POST```

```
{
    'username': string, 
    'password': string
}
```

### Refresh Token

```/api/auth/jwt/refresh/ POST```

```
    {
        'refresh': string
    }
```

### Blacklist Token (Logout)

```/api/auth/jwt/blacklist/ POST```

```
    {
        'refresh': string
    }
```

### Register Account

```/api/auth/users/ POST```

```
{
    'username': string, 
    'password': string,
    'password': string,
    're_password': string
}
```

Username can be upto 30 characters and include letters, numbers, _, ., and -.

### Change password

```/api/auth/change-password POST```

```
{
    'old_password': string,
    'new_password': string,
    'new_password2': string
}
```

### Follow / Unfollow

```/api/auth/follow/:username/ POST```

Calling this URL if a user is already following an account will return `204 NO CONTENT` which results in the user being unfollowed. `201 CREATED` means that the user has been followed.

If the username doesn't exist it will return `404 NOT FOUND`.

### Get Followers

```/api/auth/followers/:username/ GET```

Returns a users followers.

### Get Following

```/api/auth/following/:username/ GET```

Return the accounts that a user is following.

### Block a user

```/api/auth/block/:username/ POST```

Calling this URL if a user is already following an account will return `204 NO CONTENT` which results in the user being unblocked. `201 CREATED` means that the user has been blocked.

If the username doesn't exist it will return `404 NOT FOUND`.
