from django.shortcuts import render, get_object_or_404
from django.http import Http404, JsonResponse

from Auth import models

# Create your views here.
def productPayment(request, id):
    if not request.user.is_authenticated:
        raise Http404('Invalid Request')
    
    product = get_object_or_404(models.Product, code=id)
    context = {
        'product':product

    }
    return render(request, 'payment.html', context)
