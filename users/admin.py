from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Profile

# Register your models here.

class ProfileAdmin(UserAdmin):
    model = Profile
    list_display = [
        'username',
        'email',
        'first_name',
        'last_name',
        'is_active',
        'date_joined',
        'is_staff',
    ]
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': (
            'profile_picture',
            'private_account',
            'website',
            'bio',
        )}),
    )


admin.site.register(Profile, ProfileAdmin)
