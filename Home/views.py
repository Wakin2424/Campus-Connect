from django.shortcuts import render, redirect

# Create your views here.
def Auth_index(request):
    pass

def Unauth_index(request):
    return render(request, 'index.html')

def Index(request):
    if request.user.is_authenticated:
        return Auth_index(request)
    else:
        return Unauth_index(request)
    

