from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.productPayment, name='payment'),
    path('<str:id>/', views.productPayment, name='payment'),
    path('api/inter-payment-processing/<str:id>/', views.productPaymentProcessing, name='inter_payment_processing'),
    path('api/payment-negotiation/', views.paymentNegotiationRequest, name='payment_negotiation_request'),
    path('redirect', views.paymentRedirect, name='redirect'),
    path('paypal', include('paypal.standard.ipn.urls')),
    path('payment-success', views.successTemplate, name='payment_success'),
    path('payment-fail', views.failTemplate, name='payment_fail'),
    path('test', views.Test, name='payment_test')
]