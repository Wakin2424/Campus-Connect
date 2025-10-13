from django.urls import path
from . import views

urlpatterns = [
    path('', views.Login, name='login'),
    path('signup', views.Signup, name='signup'),
    path('logout', views.Logout, name='logout'),
    path('edit-profile', views.Edit, name='edit_profile')
]
