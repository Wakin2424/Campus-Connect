from django.shortcuts import render, redirect
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from . import models
import json, os, uuid

# Create your views here.
def Home(request):
    return render(request, 'qa.html')

def Question_form(request):
    if not request.user.is_authenticated:
        raise Http404('invalid request')
    
    if request.method == 'POST':
        user = models.AuthCustomuser.objects.get(id=request.user.id)
        data = request.POST.copy()
        images = request.FILES.items()

        question = models.Qa.objects.create(user=user,question=data['question'], description=data['description'], code=uuid.uuid4())
        courseDataset = str(data['courses']).split(',')

        for courseData in courseDataset:
            if len(models.Course.objects.filter(course_name=courseData)) > 0:
                course = models.Course.objects.get(course_name=courseData)
                subject = models.QuestionSubjects(course=course, question=question)
                subject.save()


        for key, img in images:
            title = uuid.uuid4()
            ext = os.path.splitext(img.name)[1]
            img.name = f'{title}.{ext}'
            image = models.Images.objects.create(title = title, file=img)
            image.save()
            image_ref = models.ImageReference.objects.create(question=question, image=image)
            image_ref.save()
            
        status = True
        url = f'{request.build_absolute_uri("question")}/{question.code}'
        context = {
            'status':status,
            'url': url
        }
        return JsonResponse(context)

    else:
        courses = models.Course.objects.all()
        context = {
            'courses':courses
        }
        return render(request, 'question_form.html', context)

def Question(request, id):
    question = get_object_or_404(models.Qa, code=id)
    User = get_user_model()
    user = User.objects.get(id=question.user.id)
    courses = models.QuestionSubjects.objects.filter(question=question)
    images_list = models.ImageReference.objects.filter(question=question)
    images = []
    if len(images_list) > 0:
        for img in images_list:
            images.append(img.image.file.url)
        

    question.views += 1
    question.save()
    context = {
        'seeker':user,
        'question':question,
        'courses' :courses,
        'images'  :json.dumps({'images':images})

    }
    return render(request, 'question_detail.html', context)

def Answer(request, id):
    if request.method == 'POST':
        status = False
        try:
            question = models.Qa.objects.get(code=id)
        except:
            return JsonResponse({'status':status})

        jsondata = {
            'username':"",
            'fullname': "",
            'acronym':"",
            'answer':"",
            'votes': 1,
            'created_at':'',

        }
        url = f'{request.build_absolute_uri('answer')}/{id}'
        question.answers
        pass
    pass