from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='notes'),
    path('upload-note', views.Note_Upload, name='note_upload'),
    path('api/load-notes/', views.LoadHomeData, name='load_notes'),
    path('<str:id>/', views.Note_Detail, name='note_detail'),
    path('api/courses/', views.GetAllCourses, name='get_all_courses'),
    path('api/notesDetail/<str:id>/', views.notesDetailsApi, name='notes_details_api'),
]