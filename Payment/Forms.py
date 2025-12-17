from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from django.urls import reverse


def mpesaPaymentProcessing(request, product):
    return

def paypalPaymentProcessing(request, payment):
    host = request.get_host()
    paypal_info = {
        'business' : settings.PAYPAL_RECIEVER_EMAIL,
        'amount' : payment.price/129.4,
        'item_name': payment.product.name,
        'no_shipping': '2',
        'invoice' : payment.transaction_id,
        'currency_code': 'USD',
        'notify_url': 'https://{}{}'.format(host, reverse('paypal-ipn')),
        'return_url': 'https://{}{}'.format(host, reverse('payment_success')),
        'cancel_url': 'https://{}{}'.format(host, reverse('payment_fail'))
    }

    return PayPalPaymentsForm(initial=paypal_info)
