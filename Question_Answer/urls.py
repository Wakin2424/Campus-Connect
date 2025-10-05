from django.urls import path 
from . import views

urlpatterns = [
    path('', views.Home, name='question_library'),
    path('question', views.Question_form, name='question'),
    path('question/<str:id>/', views.Question, name='question'),
    path('answer/<str:id>/', views.Answer, name='answer')
]
