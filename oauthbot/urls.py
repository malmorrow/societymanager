from django.contrib import admin
from django.urls import include, path

urlpatterns = [
	path('', include('pages.urls')),

    path('admin/', admin.site.urls),

	path('users/', include('users.urls')),
	path('accounts/', include('allauth.urls')),
    path('cosmo/', include('telegramsocietybot.urls', namespace='telegramsocietybot')),
]
