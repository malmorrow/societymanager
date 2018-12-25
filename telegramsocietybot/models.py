from django.db import models
from django.contrib.auth.models import User, UserManager
from django.utils import timezone

from django.conf import settings


class TelegramUserManager(UserManager):
	
	pass


class TelegramUser(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	#user_id = models.IntegerField(unique=True)

	#def __str__(self):
	#	return f'{self.user_id}'


class Message(models.Model):
    update_id   = models.IntegerField(unique=True)
    text        = models.TextField(max_length=4096)
    date        = models.DateTimeField(default=timezone.now)
    sender      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.text}'
