from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse

# Create your views here.
def Home(request):
    return render(request, 'notes.html')


def LoadHomeData(request):
    return

def Note_Detail(request, id):
    return render(request, 'notes_details.html')

def Note_Upload(request):
    pass