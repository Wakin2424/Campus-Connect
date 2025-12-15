from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, JsonResponse
from django.urls import reverse
from Auth import models
import uuid, json

# Create your views here.
def mpesaPaymentProcessing(request, product):
    pass

def paypalPaymentProcessing(request, address, product):
    pass

def productPaymentProcessing(request, id):
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
    if payment_method == 'paypal' or payment_method == 'mpesa':
        payment = models.Payment(transaction_id=transaction_id, user=user, product=product, payment_method=payment_method, price=product.discount)
        address = models.Address(user=user, address1=address1, address2=address2, contact=contact, city=city, postal_code=postal_code, country=country)

        payment.save()
        address.save()

        if payment_method == 'paypal':
            return paypalPaymentProcessing(request, address, product)
        else:
            return mpesaPaymentProcessing(request, product)
        
    elif payment_method == 'contactSeller':
        payment = models.Payment(transaction_id=transaction_id, user=user, product=product, payment_method='negotiate', price=product.discount)
        return redirect(reverse('product_detail', kwargs={'id': product.code}))


def productPayment(request, id):
    if not request.user.is_authenticated:
        raise Http404('Invalid Request')
    
    if request.method == 'POST':
        productPaymentProcessing(request, id)


    product = get_object_or_404(models.Product, slug=id)
    discount = round((product.price - product.discount)/product.price *100, 0)
    context = {
        'product':product,
        'discount':discount

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