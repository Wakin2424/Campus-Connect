from django.urls import path
from . import views

urlpatterns = [
    path('', views.productPayment, name='payment'),
    path('<str:id>/', views.productPayment, name='payment'),
    path('api/inter-payment-processing/<str:id>/', views.productPaymentProcessing, name='inter_payment_processing'),
    path('api/payment-negotiation/', views.paymentNegotiationRequest, name='payment_negotiation_request'),
    path('test', views.Test, name='payment_test')
]