from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404

# Create your views here.
def Home(request):
    return render(request, 'market.html')

def productLibrary(request, category):
    context = {}
    return render(request, 'product_library.html', context)

def loadProducts(request):
    pass

def uploadProduct(request):
    if not request.user.is_authenticated:
        raise Http404("Invalid Request!")
    
    if request.method == "POST":
        pass
    
    else:
        context = {}
        return render(request, 'sell_product.html', context)

def productDetail(request, id):
    context = {}
    return render(request, 'product_detail.html', context)
