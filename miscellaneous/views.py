from django.shortcuts import render

# Create your views here.
def about(request):
    return render(request, 'miscellaneous/about-us.html')

def termsAndConditions(request):
    return render(request, 'miscellaneous/terms-conditions.html')