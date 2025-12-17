from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from . import Forms
from django.contrib.auth import get_user_model
from django.urls import reverse
from Auth import models
import uuid, json

fee = 200
# Create your views here.

def productPaymentProcessing(request, id):
    if request.method == 'POST':
        product = get_object_or_404(models.Product, code=id)
        user = models.AuthCustomuser.objects.get(id=request.user.id)
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        contact = request.POST.get('contact')
        city = request.POST.get('city')
        postal_code = request.POST.get('postalCode')
        country = request.POST.get('country')
        payment_method = request.POST.get('paymentMethod')
        transaction_id = uuid.uuid4().hex[:12].upper()

        payment = models.Payment(transaction_id=transaction_id, user=user, product=product, payment_method=payment_method, price=product.discount)
        address = models.Address(user=user, address1=address1, address2=address2, contact=contact, city=city, postal_code=postal_code, country=country)
        
        request.session['payment'] = True

        if payment_method == 'paypal' or payment_method == 'mpesa':
            payment = models.Payment(transaction_id=transaction_id, user=user, product=product, payment_method=payment_method, price=product.discount+fee)
            address = models.Address(user=user, address1=address1, address2=address2, contact=contact, city=city, postal_code=postal_code, country=country)

            payment.save()
            address.save()

            return JsonResponse({'status':True})
            
        elif payment_method == 'seller':
            payment = models.Payment(transaction_id=transaction_id, user=user, product=product, payment_method='negotiate', price=product.discount)
            return redirect(reverse('product_detail', kwargs={'id': product.code}))



def productPayment(request, id):
    if not request.user.is_authenticated:
        raise Http404('Invalid Request')

    product = get_object_or_404(models.Product, slug=id)
    User = get_user_model()
    seller = User.objects.get(id=product.user.id)
    discount = round((product.price - product.discount)/product.price *100, 0)
    context = {
        'product':product,
        'seller': seller,
        'discount':discount,
        'fee':fee

    }
    return render(request, 'payment.html', context)

def paymentNegotiationRequest(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            payment_request = models.Payment.objects.get(transaction_id=data.get('id'))
            
            if data.get('status'):
                payment_request.status = 'complete'
                payment_request.save()
                return JsonResponse({'status':True})
            else:
                payment_request.status = 'cancelled'
                payment_request.save()
                return JsonResponse({'status':False})
            
        except:
            return JsonResponse({'status':False})
    return JsonResponse({'status':False})

def Test(request):
    if request.method=='POST':
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        contact = request.POST.get('contact')
        city = request.POST.get('city')
        postal_code = request.POST.get('postalCode')
        country = request.POST.get('country')
        payment_method = request.POST.get('paymentMethod')

        print(address1, address2, contact, city, postal_code, country, payment_method)

    return JsonResponse({'stauts':False})

def paymentRedirect(request):
    if not request.user.is_authenticated or not request.session.get('payment'):
        raise Http404('Invalid Request')
    
    user = models.AuthCustomuser.objects.get(id=request.user.id)
    payment = models.Payment.objects.filter(user=user, status='pending')
    
    if len(payment) == 0:
        raise Http404('Invalid Request')
    
    payment = payment.last()
    context = {}

    if payment.payment_method == 'paypal':
        context['Type'] = 'paypal'
        context['paypal_form'] = Forms.paypalPaymentProcessing(request, payment)
    
    elif payment.payment_method == 'mpesa':
        pass 

    return render(request, 'redirect.html', context)

#mpesa callback function
@csrf_exempt
def mpesaCallback(request):
    data = json.loads(request.body)
    result_code = data['Body']['stkCallback']['ResultCode']

def successTemplate(request):
    pass

def failTemplate(request):
    pass