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


class CommandReceiveView(View):

	def _display_help():
		return render_to_string('help.md')

	commands = {
		'/start': _display_help,
		'help': _display_help,
	}

	def post(self, request, bot_token):
		if bot_token != settings.TELEGRAM_BOT_TOKEN:
			return HttpResponseForbidden('Invalid token')

		raw = request.body.decode('utf-8')
		logger.info(raw)

		try:
			payload = json.loads(raw)
		except ValueError:
			return HttpResponseBadRequest('Invalid request body')
		else:
			chat_id = payload['message']['chat']['id']
			cmd = payload['message'].get('text')

			func = commands.get(cmd.split()[0].lower())

			if func:
				bot.sendMessage(chat_id, func(), parse_mode='Markdown')
			else:
				bot.sendMessage(chat_id, 'I do not understand that command.')

		return JsonResponse({}, status=200)

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super(CommandReceiveView, self).dispatch(request, *args, **kwargs)
