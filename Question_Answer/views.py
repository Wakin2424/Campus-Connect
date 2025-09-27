from django.shortcuts import render, redirect
from django.http import Http404, JsonResponse
import json

# Create your views here.
def Home(request):
    return render(request, 'qa.html')

def Question_form(request):
    if not request.user.is_authenticated:
        raise Http404('invalid request')
    
    if request.method == 'POST':
        data = dict(json.loads(request.body))
        status = False
        url = ''
        context = {
            'status':status,
            'url': url
        }
        return JsonResponse(context)

    else:
        return render(request, 'question_form.html')

def Question(request, id):
    context = {

    }
    return render(request, 'question_detail.html', context)