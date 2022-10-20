# Notifications 

## Endpoints

The layout for each each point is 

```URL METHOD```

```
{ 
    POST Dict 
}
```

### Get all 

```/api/notifications/all/ GET```

Paginated response of a users notifications, read and unread.

### Get notification

```/api/notifications/:notification_id GET```

### Mark as read

```/api/notifications/:notification_id POST```

### Mark as unread

```/api/notifications/:notification_id POST```

### Mark all as read

```/api/notifications/:notification_id POST```

