from django.conf import settings
from django.template.loader import render_to_string
from django.http import HttpResponseForbidden, HttpResponseBadRequest, JsonResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from datetime import datetime
import json
import logging

import telepot

from .models import TelegramUser, Message

bot = telepot.Bot(settings.TELEGRAM_BOT_TOKEN)

logger = logging.getLogger('telegram.bot')


def _display_help(payload=None):
	return render_to_string('help.md')

def _register(payload):
	if payload['message']['from'].get('is_bot') is True:
		return 'I cannot register bots as members.'
	from_id = payload['message']['from']['id']
	username = payload['message']['from'].get('username')
	is_bot = payload['message']['from'].get('is_bot')
	first_name = payload['message']['from'].get('first_name')
	last_name = payload['message']['from'].get('last_name')

	return render_to_string('signup.html')


class CommandReceiveView(View):

	def post(self, request, bot_token):
		if bot_token != settings.TELEGRAM_BOT_TOKEN:
			return HttpResponseForbidden('Invalid token')

		commands = {
			'/start': 		_display_help,
			'/register':	_register,
			'help': 		_display_help,
		}
		raw = request.body.decode('utf-8')
		logger.info(raw)

		try:
			payload = json.loads(raw)
		except ValueError:
			return HttpResponseBadRequest('Invalid request body')
		else:
			text = payload['message'].get('text')
			from_id = payload['message']['from']['id']

			func = commands.get(text.split()[0].lower())

			if func:
				bot.sendMessage(from_id, func(payload), parse_mode='Markdown')
			else:
				bot.sendMessage(from_id, 'I do not understand that command.')

		return JsonResponse({}, status=200)

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super(CommandReceiveView, self).dispatch(request, *args, **kwargs)
