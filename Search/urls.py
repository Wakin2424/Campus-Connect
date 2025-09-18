from django.urls import path
from . import views

urlpatterns = [
    path('', views.Search_all, name='search'),
    path('<str:text>/', views.Search, name='search')
]
