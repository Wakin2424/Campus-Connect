from django.urls import path
from . import views

urlpatterns = [
    path('<str:id>/', views.productPayment, name='payment'),
    path('api/payment-negotiation/', views.paymentNegotiationRequest, name='payment_negotiation_request'),
]