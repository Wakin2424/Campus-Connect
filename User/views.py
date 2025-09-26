from django.shortcuts import render, redirect
from django.http import Http404
from django.shortcuts import get_object_or_404
from . import models


# Create your views here.
def Myprofile(request):
    if not request.user.is_authenticated:
        raise Http404('Invalid Request')
    
    return render(request, 'profile.html')

def Otherprofile(request, account):
    try:
        user = models.AuthCustomuser.objects.get(username=account)
        return render(request, 'user.html')
    
    except:
        raise Http404('There is no such account')