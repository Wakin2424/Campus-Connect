from django.shortcuts import render, redirect
from django.http import JsonResponse
import json

# Create your views here.
def Auth_index(request):
    return render(request, 'home.html')

def Unauth_index(request):
    return render(request, 'index.html')

def Home(request):
    if request.user.is_authenticated:
        return Auth_index(request)
    else:
        return Unauth_index(request)

def Test_page(request):
    if request.method == 'POST':
        dataset = dict(json.loads(request.body))
        data = dataset['dataset']
        images = dataset['images']
        
        print(data, images)
        context = {
            'status':True,
            'data':data
        }
        return JsonResponse(context)
    return render(request, 'test.html')
    

