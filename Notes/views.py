from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse, JsonResponse
from Auth import models

# Create your views here.
def Home(request):
    return render(request, 'notes.html')


def LoadHomeData(request):
    return

def Note_Detail(request, id):
    return render(request, 'notes_details.html')

def Note_Upload(request):
    if request.method == 'POST':
        dataset = request.POST.copy()
        file = request.FILES.items()
        status = False
        print(dataset, file)

        context = {
            'status' : status,
            'url' : ''
        }
        return JsonResponse(context)
    return render(request, 'upload_notes.html')