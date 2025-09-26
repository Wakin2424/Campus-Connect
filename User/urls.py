from django.urls import path
from . import views

urlpatterns = [
    path('', views.Myprofile, name='user'),
    path('<str:account>/', views.Otherprofile, name='user')
]
