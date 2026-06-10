from django.urls import path
from . import views
from rest_framework_simplejwt.views import ( TokenObtainPairView, TokenRefreshView,)


urlpatterns = [
    path('', views.Login, name='login'),
    path('signup', views.Signup, name='signup'),
    path('logout', views.Logout, name='logout'),
    path('edit-profile', views.EditProfile, name='edit_profile'),
    path('forgot-password', views.forgotPassword, name='forgot_password'),
    path('reset-password/<str:uidb64>/<str:token>/', views.resetPassword, name='reset_password'),
    path('reset-password/success/', views.resetPasswordSuccess, name='reset_password_success'),
    path('reset-password/failed/', views.resetPasswordFailed, name='reset_password_fail'),
    ### JWT Authentication
    path("api/token/", TokenObtainPairView.as_view()),
    path("api/token/refresh/", TokenRefreshView.as_view()),
    path('api/login', views.JWTLoginView)
]
