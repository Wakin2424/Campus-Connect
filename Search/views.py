from django.shortcuts import render

# Create your views here.
def Search(request):
    result=request.GET['result']
    questions = None
    notes = None
    products = None
    context = {
        'result':result,
        'questions': questions, 
        'notes':notes,
        'products':products
    }
    return render(request, 'search.html', context)
