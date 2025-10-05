from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from . import models


# Create your views here.
def Myprofile(request):
    if not request.user.is_authenticated:
        raise Http404('Invalid Request')
    
    return render(request, 'profile.html')

def Otherprofile(request, account):
    try:
        User = get_user_model()
        user = User.objects.get(username=account)
        user = models.AuthCustomuser.objects.get(username=account)
    except:
        raise Http404('There is no such account')
    
    questions = models.Qa.objects.filter(user=user).values('question', 'views', 'likes', 'code', 'created_at')
    print(questions)
    context = {
        'account':user,
        'questions': questions
    }
    return render(request, 'user.html', context)
    