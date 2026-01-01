from django.urls import path
from . import views


urlpatterns = [
    path('', views.groupHomeRender, name='group_home'),
]