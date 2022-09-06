# Profile Auth App

## Endpoints

The layout for each each point is 

```URL METHOD```

```
{ 
    POST Dict 
}
```

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

### Change password

```/api/auth/change-password POST```

```
{
    'old_password': string,
    'new_password': string,
    'new_password2': string
}
```
