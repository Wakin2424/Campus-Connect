from django.shortcuts import render

# Create your views here.
def Home(request):
    return render(request, 'qa.html')

def Question_form(request):
    if request.method == 'POST':
        pass

    else:
        return render(request, 'questionform.html')