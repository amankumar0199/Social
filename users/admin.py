from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .models import FriendRequest, Friendship

admin.site.register(FriendRequest)
admin.site.register(Friendship)