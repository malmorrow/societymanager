from django.urls import path

from .views import CommandReceiveView

app_name = 'telegramsocietybot'

urlpatterns = [
    path('bot/(?P<bot_token>.+)/$', CommandReceiveView.as_view(), name='command'),
]
