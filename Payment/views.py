from django.shortcuts import render, get_object_or_404

from Auth import models

# Create your views here.
def productPayment(request, id):
    product = get_object_or_404(models.Product, code=id)
    context = {
        'product':context
    }
    return render(request, 'payment', context)
