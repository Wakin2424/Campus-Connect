from django.shortcuts import render

# Create your views here.
def websocketTest(request):
    return render(request, 'test.html')