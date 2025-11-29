from django.shortcuts import render, redirect
from django.http import JsonResponse
from Auth import models
import json

# Create your views here.
def Auth_index(request):
    user = models.AuthCustomuser.objects.get(id=request.user.id)
    question_length = len(models.Qa.objects.filter(user=user))
    answer_length = len(models.Answers.objects.filter(user=user))
    latest_questions = models.Qa.objects.all().order_by('-created_at')[:6 if len(models.Qa.objects.all()) > 6 else len(models.Qa.objects.all())]
    trending_questions = models.Qa.objects.all().order_by('-views')[:6 if len(models.Qa.objects.all()) > 6 else len(models.Qa.objects.all())]
    
    context = {
        'question_length': question_length,
        'answer_length': answer_length,
        'latest_questions': latest_questions,
        'trending_questions': trending_questions,
    }
    return render(request, 'home.html', context)

def Unauth_index(request):
    return render(request, 'index.html')

def Home(request):
    if request.user.is_authenticated:
        return Auth_index(request)
    else:
        return Unauth_index(request)

    

