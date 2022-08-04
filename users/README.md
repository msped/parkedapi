# Profile Auth App

## Endpoints for Users

### Obtain Token (Login)

```/api/auth/jwt/create/ POST```

Taking the `username` and `password` as post parameters.

### Refresh Token

```/api/auth/jwt/refresh/ POST```

Taking the `refresh` token as a post parameter.

### Blacklist Token (Logout)

```/api/auth/jwt/blacklist/ POST```

Taking `refresh` token as a post parameter.

### Register Account

```/api/auth/users/ POST```

Taking `username`, `email`, `password` and `re_password` as post parameters.

### Change password

```/api/auth/change-password POST```

Taking `old_password`, `new_password` and `new_password2` as post parameters.
