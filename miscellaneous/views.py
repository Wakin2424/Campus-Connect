from django.shortcuts import render

# Create your views here.
def about(request):
    return render(request, 'miscellaneous/about.html')

def termsAndConditions(request):
    return render(request, 'terms-and-condition.html')