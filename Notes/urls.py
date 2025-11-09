from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='notes'),
    path('upload-note', views.Note_Upload, name='note_upload'),
    path('<str:id>/', views.Note_Detail, name='note_detail'),
]