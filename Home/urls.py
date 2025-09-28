from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='home'),
    path('test', views.Test_page, name='test')
]
