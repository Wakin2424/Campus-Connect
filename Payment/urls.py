from django.urls import path
import views

url_patterns = [
    path('<str:id>/', views.productPayment, name='payment')
]