from django.urls import path 
from . import views

urlpatterns = [
    path('', views.Home, name='question_library'),
    path('question', views.Question_form, name='question'),
    path('question/<str:id>/', views.Question, name='question'),
    path('answer/', views.Answerhome, name='answerRedirect'),
    path('answer/<str:id>/', views.Answer, name='answer'),
    path('answer/AI/<str:id>/', views.AIanswer, name='AIanswer'),
    path('api/load/questions', views.Load_questions, name='load_questions'),
    path('api/load/votes', views.Vote, name='vote')
]
