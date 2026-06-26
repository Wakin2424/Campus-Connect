from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from Auth import models
from rest_framework.decorators import api_view

# Create your views here.
def websocketTest(request):
    return render(request, 'test.html')

@api_view(['GET'])
def loadDataApi(request, slug):
    print(request.user)
    if not request.user.is_authenticated:
        return JsonResponse({'status':False}, status=403)
    
    try:
        group = get_object_or_404(models.Group, slug=slug)
        messages = models.GroupMessages.objects.get(group=group)

        
        context = {
            'group_name': group.name,
            'group_image': group.image.file.url,
            'admin': {
                'first_name': group.admin.first_name,
                'last_name': group.admin.last_name,
                'email': group.admin.email,
                'image': group.admin.image.file.url,
            },
            'messages': list(messages.messages),
        }
        
        return JsonResponse(context, status=200)
    
    except Exception as e:
        print(e)
        return JsonResponse({}, status=500)