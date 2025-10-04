# views.py
from django.http import JsonResponse

def upload(request):
    if request.method == "POST":
        text_content = request.POST.get("content")
        images = request.FILES.getlist("images")  # multiple files

        for img in images:
            # Save to model
            MyModel.objects.create(text=text_content, image=img)

        return JsonResponse({"status": "ok"})
