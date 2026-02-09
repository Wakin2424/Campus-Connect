from django.urls import path
from . import views

url_patterns = [
    path('/question/answer/<str:id>/', views.AIanswer, name='AIanswer'),
]