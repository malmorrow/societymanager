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

def _display_help():
	return render_to_string('help.md')


class CommandReceiveView(View):

	def post(self, request, bot_token):
		if bot_token != settings.TELEGRAM_BOT_TOKEN:
			return HttpResponseForbidden('Invalid token')

		commands = {
			'/start': _display_help,
			'help': _display_help,
		}
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

@csrf_exempt
def message_to_bot(request):
    try:
        json_message = json.loads(request.body)
    except json.decoder.JSONDecodeError as err:
        return HttpResponse(str(err))

    def _is_user_registered(user_id: int) -> bool:
        if User.objects.filter(user_id__exact=user_id).count() > 0:
            return True
        return False

    def _update_id_exists(update_id: int) -> bool:
        if Message.objects.filter(update_id__exact=update_id).count() > 0:
            return True
        return False

    def _add_message_to_db(json_dict: dict) -> (None, True):
        try:
            sender_id       = json_dict['message']['from'].get('id')
            sender_object   = User.objects.filter(user_id__exact=sender_id).get()
            update_id       = json_dict.get('update_id')
            message_text    = json_dict['message'].get('text')
            message_date    = json_dict['message'].get('date')
        except KeyError:
            return None
        if None in (sender_id, update_id, message_text, message_date):
            return None

        if _update_id_exists(update_id):
            return True

        if _is_user_registered(sender_id):
            try:
                Message(
                    update_id=int(update_id),
                    text=str(message_text),
                    sender=sender_object,
                    date=datetime.fromtimestamp(int(message_date)),
                ).save()
                return True
            except (KeyError, ValueError):
                return None
        else:
            raise ValueError('Sender is rejected')
                
    try:
        result = _add_message_to_db(json_message)
    except ValueError as err:
        return HttpResponseBadRequest(str(err))
    if result is True:
        return HttpResponse("OK.")
    else:
        return HttpResponseBadRequest("Malformed or incomplete JSON data received.")
