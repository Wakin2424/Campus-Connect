from django.urls import path
from . import views

urlpatterns = [
    path('test', views.websocketTest, name='test'),
    path('load-data/api/<str:slug>/', views.loadDataApi, name='load_data_api'),
]