"""
URL configuration for Campus_Connect project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Home.urls')),
    path('auth/', include('Auth.urls')),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('user/', include('User.urls')),
    path('search/', include('Search.urls')),
    path('question-answer/', include('Question_Answer.urls')),
    path('notes/', include('Notes.urls')),
    path('market/', include('Market.urls')),
    path('payment/', include('Payment.urls')),
    path('Groups/', include('Groups.urls')),
    path('chat/', include('chat.urls')),
    path('api/mails/', include('Mail.urls')),
    path('api/ai/modulo/', include('AI_model.urls')),
    path('info/', include('miscellaneous.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)