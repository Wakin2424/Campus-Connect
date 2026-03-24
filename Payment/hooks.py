from django.apps import AppConfig
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver
from django.conf import settings
from requests.auth import HTTPBasicAuth
import requests, base64, datetime, json


#### Paypal Functionality
class PaymentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Payments'

    def ready(self):
        import Payment.hooks

@receiver(valid_ipn_received)
def Paypal_payment_received(sender, **kwargs):
    paypal_obj = sender 
    print(f'amount: {paypal_obj.mc_gross}')


#### M-pesa Functionality
# Get mpesa token
def normalizePhone(phone):
    phone = phone.strip().replace(" ", "")

    if phone.startswith("0"):
        return "254" + phone[1:]

    if phone.startswith("+254"):
        return phone[1:]

    if phone.startswith("254"):
        return phone

    raise ValueError("Invalid phone number format")


def getMpesaToken():
    url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    response = requests.get(url, auth=HTTPBasicAuth(settings.MPESA_CUSTOMER_KEY, settings.MPESA_CUSTOMER_SECRET))
    print(f"Got the access token: {response.json().get('access_token')}")
    return response.json().get('access_token')

# Initiate STK push Function
def initiateStkPush(callback_uri, phone_number, product_name, amount):
    access_token = getMpesaToken()
    phone_number = normalizePhone(phone_number)
    print(access_token, 'hello', phone_number, callback_uri, amount)
    amount = int(amount)
    
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    password = base64.b64encode((settings.MPESA_SHORTCODE + settings.MPESA_PASSKEY + timestamp).encode()).decode()
    headers = {
        'Authorization': f"Bearer {access_token}",
        'Content-Type': "application/json"
    }

    payload = {
        'BusinessShortCode': settings.MPESA_SHORTCODE,
        'Password':password,
        'Timestamp':timestamp,
        'TransactionType': 'CustomerPayBillOnline',
        'Amount':amount,
        'PartyA':phone_number,
        'PartyB':settings.MPESA_SHORTCODE,
        'PhoneNumber':phone_number,
        'CallBackURL': callback_uri,
        'AccountReference': 'Ref123',
        'TransactionDesc': f'Campus Connect-payment: {product_name}'
    }

    response = requests.post(
        'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest',
        headers=headers,
        json=payload
    )

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.text)

    return response.json()