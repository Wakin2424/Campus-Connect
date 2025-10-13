from django.shortcuts import render, redirect
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from . import models
import json, os, uuid
import datetime as dt

# Create your views here.
def Home(request):
    tags = models.QuestionSubjects.objects.all().order_by()
    trending = models.Qa.objects.all()
    resents = models.Qa.objects.all()
    resents = resents.order_by('-created_at')[:4 if len(trending) >= 4 else len(trending)]
    trending = trending.order_by('-likes')[:3 if len(trending) >= 3 else len(trending)] 
    
    context = {
        'trending':trending,
        'tags':tags,
        'resents':resents
    }
    return render(request, 'qa.html', context)

def Load_questions(request):
    try:
        page = int(request.GET.get('page'))
    except:
        raise Http404('Invalid Request')
    status = True

    questions = models.Qa.objects.all().values('qa_id','question', 'description', 'answer_len', 'views', 'user__first_name', 'code','created_at')
    length = len(questions)

    if page+1 < int(length/5):
        start = page * 5
        end = start + 5
        page = int(end/5)
        questions = questions[start:end]

    else:
        status = False
        questions = questions[length-5 if length >= 5 else 0:]

    questions = list(questions)
    for question in questions:
        question['courses'] = []
        quiz = models.Qa.objects.get(qa_id=question['qa_id'])
        courses = list(models.QuestionSubjects.objects.filter(question=quiz).values('course__course_name'))
        for course in courses:
            question['courses'].append(course['course__course_name'])

        del question['qa_id']
        
    context = {
        'status':status,
        'page':page,
        'questions':questions
    }
    return JsonResponse(context)

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
        'id':id,
        'question':question,
        'courses' :courses,
        'images'  :json.dumps({'images':images}),
        'answers' : question.answers

    }
    return render(request, 'question_detail.html', context)

def Answerhome(requeest):
    return redirect('question_library')

def Answer(request, id):
    if not request.user.is_authenticated or not request.user.is_verified:
        raise Http404('Invalid Request. Please ensure you are a verified member')
    
    if request.method == 'POST':
        status = True
        try:
            question = models.Qa.objects.get(code=id)
        except:
            status = False
            return JsonResponse({'status':status})
        

        user = models.AuthCustomuser.objects.get(id=request.user.id)
        data = request.POST.copy()
        imageset = request.FILES.items()

        images = []

        for key, img in imageset:
            title = uuid.uuid4()
            ext = os.path.splitext(img.name)[1]
            img.name = f'{title}.{ext}'
            image = models.Images.objects.create(title = title, file=img)
            image.save()
            images.append(image.file.url)
            image_ref = models.ImageReference.objects.create(question=question, image=image)
            image_ref.save()

        jsondata = {
            'username':question.user.username,
            'fullname': f"{question.user.first_name} {question.user.last_name}",
            'acronym':f"{str(question.user.first_name).upper()[0]}{str(question.user.last_name).upper()[0]}",
            'answer':data['answer'],
            'votes': 1,
            'images':images,
            'created_at': dt.datetime.now().isoformat(),
        }

        if question.answers is None:
            question.answers = {}

        question.answers[str(uuid.uuid4())] = jsondata
        question.answer_len += 1
        question.save()

        url = request.build_absolute_uri(f"/question-answer/question/{id}/")
        context = {
                'status':status,
                'url': url
            }

        return JsonResponse(context)
    
    else:
        try:
            question = models.Qa.objects.get(code=id)
        except:
            raise Http404("There is no such question")
        
        images_list = models.ImageReference.objects.filter(question=question)
        images = []
        if len(images_list) > 0:
            for img in images_list:
                images.append(img.image.file.url)
        
        context = {
            'question':question,
            'images'  : images,
            }
        return render(request, 'answer.html', context)

def Vote(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id = data['id']
        Type = data['Type']

        context = {
            'status':True
            }

        if Type == 'question':
            question = models.Qa.objects.get(code=id)
            question.likes += 1
            vote = question.likes
            question.save()
            context['vote'] = vote

        elif Type == 'answer':
            question = models.Qa.objects.get(code=id)
            question.answers[data['answer']]['votes'] += 1
            vote = question.answers[data['answer']]['votes']
            question.save()
            context['vote'] = vote
        
        elif Type == 'rating':
            rating = int(data['rating'])
            question = models.Qa.objects.get(code=id)

        return JsonResponse(context)
    return JsonResponse({'status':False})