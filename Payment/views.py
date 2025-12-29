from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, JsonResponse, HttpResponseForbidden, HttpResponseNotAllowed
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
        return redirect('login')

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
        raise HttpResponseForbidden('')
    
    user = models.AuthCustomuser.objects.get(id=request.user.id)
    payment = models.Payment.objects.filter(user=user, status='pending')
    address = models.Address.objects.filter(user=user).last()
    
    if len(payment) == 0:
        raise HttpResponseForbidden('')
    
    payment = payment.last()
    context = {}

    if payment.payment_method == 'paypal':
        context['Type'] = 'paypal'
        context['paypal_form'] = Forms.paypalPaymentProcessing(request, payment)
    
    elif payment.payment_method == 'mpesa':
        Forms.mpesaPaymentProcessing(request, payment, address.contact)

    return render(request, 'redirect.html', context)

#mpesa callback function
@csrf_exempt
def mpesaCallback(request, id):
    if request.method == 'POST':
        data = json.loads(request.body)
        result_code = data['Body']['stkCallback']['ResultCode']

        payment = models.Payment.objects.get(transaction_id=id)

        if result_code == 0:
            payment.status = 'complete'
            payment.save()
        
        else:
            payment.status = 'cancelled'
            payment.save()
        
        return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})
    return JsonResponse({"error": "Invalid method"}, status=405)

def mpesaTransactionCheck(request, id):
    if request.method == 'POST':
        try:
            payment = models.Payment.objects.get(transaction_id=id)

            if payment.status == 'complete':
                url = request.build_absolute_uri(reverse('payment_success', kwargs={'slug': payment.product.slug}))
                return JsonResponse({'status': 200, 'url':url})
            
            elif payment.status == 'cancelled':
                url = request.build_absolute_uri(reverse('payment_fail', kwargs={'slug': payment.product.slug}))
                return JsonResponse({'status': 200, 'url':url})
            
            else:
                return JsonResponse({'status':204})
            
        except:
            return JsonResponse({'status':404})
        


def successTemplate(request, slug):
    product = get_object_or_404(models.Product, slug=slug)
    user = models.AuthCustomuser.objects.get(id=request.user.id)

    payment = models.Payment.objects.filter(product=product, user=user).last()

    if payment.payment_method == 'paypal':
        payment.status = 'complete'
        payment.save()

    context = {
        'product':product
    }
    return render(request, 'payment_success.html', context)

def orderReview(request):
    if not request.user.is_authenticated:
        raise HttpResponseForbidden('')
    if request.method == 'POST':
        data = json.loads(request.body)
        slug = data['slug']
        rating_value = int(data['rating'])
        review = data['review']

        try:
            product = get_object_or_404(models.Product, slug=slug)  
            user = models.AuthCustomuser.objects.get(id=request.user.id)
            rating = models.Ratings(user=user, rating=rating_value, product=product, description=review)
            rating.save()
            return JsonResponse({'status':True})
        except:
            return JsonResponse({'status':False})
    return JsonResponse({'status':False})
        
def failTemplate(request, slug):
    product = get_object_or_404(models.Product, slug=slug)
    user = models.AuthCustomuser.objects.get(id=request.user.id)

    payment = models.Payment.objects.filter(product=product, user=user).last()

    if payment.payment_method == 'paypal':
        payment.status = 'complete'
        payment.save()

    context = {
        'product':product
    }
    return render(request, 'payment_fail.html', context)

