from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import TelegramUser


class TelegramUserTestCase(TestCase):

	def setUp(self):
		self.user = get_user_model().objects.create_user('johndoe', 'john@doe.com', 'johndoe')
		self.client.login(username='johndoe', password='johndoe')

	def test_null(self):
		pass
