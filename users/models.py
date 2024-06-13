from datetime import datetime
from django.contrib.auth.models import AbstractUser, User
from django.db import models



class FriendRequest(models.Model):
    sender = models.ForeignKey(User, to_field="username", related_name='sent_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, to_field="username", related_name='received_requests', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=datetime.now())
    status = models.CharField(max_length=20, choices=(('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')))
    objects = models.Manager()
    class Meta:
        unique_together = ('sender', 'receiver')


class Friendship(models.Model):
    user1 = models.ForeignKey(User, related_name='friend1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='friend2', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=datetime.now())

    objects = models.Manager()
    class Meta:
        unique_together = ('user1', 'user2')
