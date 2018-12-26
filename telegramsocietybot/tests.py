from django.test import TestCase
from django.contrib.auth import get_user_model

from django.conf import settings

from .models import TelegramUser


class TelegramUserTestCase(TestCase):

	def setUp(self):
		self.user = get_user_model().objects.create_user('johndoe', 'john@doe.com', 'johndoe')
		self.client.login(username='johndoe', password='johndoe')

	def test_TELEGRAM_BOT_TOKEN(self):
		assert(settings.TELEGRAM_BOT_TOKEN is not None)
