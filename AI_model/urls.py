from django.urls import path
from . import views

urlpatterns = [
    path('question/answer/<str:id>/', views.AIanswer, name='AIanswer'),
]