from django.shortcuts import render

# Create your views here.
def groupHomeRender(request):
    return render(request, 'Groups/group-landing-page.html')

