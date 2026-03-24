from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from django.urls import reverse
from . import hooks


def mpesaPaymentProcessing(request, name, contact, price, transaction_id):
    callback_uri = request.build_absolute_uri(reverse('callback', kwargs={'id': transaction_id})).replace("http://", "https://")
    hooks.initiateStkPush(callback_uri, contact, name, price)

def paypalPaymentProcessing(request, payment):
    host = request.get_host()
    paypal_info = {
        'business' : settings.PAYPAL_RECEIVER_EMAIL,
        'amount' : float(payment.price)/129.4,
        'item_name': payment.product.name,
        'no_shipping': '2',
        'invoice' : payment.transaction_id,
        'currency_code': 'USD',
        'notify_url': 'https://{}{}'.format(host, reverse('paypal-ipn')),
        'return_url': 'https://{}{}'.format(host, reverse('payment_success', kwargs={'slug': payment.product.slug})),
        'cancel_url': 'https://{}{}'.format(host, reverse('payment_fail', kwargs={'slug': payment.product.slug}))
    }

    return PayPalPaymentsForm(initial=paypal_info)
