from django.db import models
from django.contrib.auth.models import User as BuiltinUser
from django.contrib.auth.validators import ASCIIUsernameValidator


class User(BuiltinUser):
    username_validator = ASCIIUsernameValidator()
    friend_list = models.CharField(max_length=2048, null = True)

class Message(models.Model):

    message_text = models.CharField(max_length=2048)
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sender'
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='receiver'
    )
    date = models.DateTimeField(
        'written_date'
    )

    def __str__(self):
        return self.message_text

class UserStatistics(models.Model):
    def __str__(self):
        return "User " + self.user.username
    positivity_percentage = models.FloatField(null = True)
    avg_time = models.CharField(max_length=2048, null = True)
    avg_text_length = models.CharField(max_length=2048, null = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
