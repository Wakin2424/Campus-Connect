from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.about, name='about'),
    path('terms-conditions/', views.termsAndConditions, name='terms_and_conditions')
]