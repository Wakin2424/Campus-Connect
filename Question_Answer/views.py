from django.shortcuts import render, redirect
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Count
import Auth.models as models
import json, os, uuid
import datetime as dt

User = get_user_model()
# Create your views here.
def Home(request):
    trend_tag = request.GET.get('tag')
    tags = models.Question_subjects.objects.values('course__course_name').annotate(count=Count('course')).order_by('-count')
    tags = tags[:6 if len(models.Question_subjects.objects.values('course__course_name').annotate(count=Count('course'))) >= 6 else len(models.Question_subjects.objects.values('course__course_name').annotate(count=Count('course')))]
    
    trending = models.Qa.objects.all()
    trending = trending.order_by('-likes')[:3 if len(trending) >= 3 else len(trending)] 
    resents = models.Qa.objects.all()
    resents = resents.order_by('-created_at')[:4 if len(trending) >= 4 else len(trending)]

    if trend_tag != 'trending':
        trending = models.Qa.objects.all()
        trending = trending.order_by('-likes')[:3 if len(trending) >= 3 else len(trending)] 
    else:
        trending = None
    
    total_questions = len(models.Qa.objects.all())
    context = {
        'trending':trending,
        'tags':tags,
        'resents':resents,
        'total_questions': total_questions
    }
    return render(request, 'QuestionAnswer/qa.html', context) 

def Load_questions(request):
    page = int(request.GET.get('page'))
    Type = request.GET.get('request')
    status = True

    if Type == 'tag':
        tag = request.GET.get('tag')
        course = models.Course.objects.get(course_name=tag)
        questions = models.Qa.objects.filter(courses=course).values('qa_id','question', 'description', 'answer_len', 'views', 'user__first_name', 'code','created_at')
    
    elif Type == 'trending':
        rating = models.Ratings.objects.filter(note=None, book=None).values('question').annotate(avg_rating=Count('rating')).order_by('-avg_rating')
        question_ids = [item['question'] for item in rating]
        questions = models.Qa.objects.filter(qa_id__in=question_ids).order_by('likes').order_by('views').values('qa_id','question', 'description', 'answer_len', 'views', 'user__first_name', 'code','created_at')
        questions = question | models.Qa.objects.exclude(qa_id__in=question_ids).order_by('-likes').values('qa_id','question', 'description', 'answer_len', 'views', 'user__first_name', 'code','created_at')
    
    elif Type == 'answered':
        questions = models.Qa.objects.all().order_by('-answer_len').values('qa_id','question', 'description', 'answer_len', 'views', 'user__first_name', 'code','created_at')

    elif Type == 'unanswered':
        questions = models.Qa.objects.filter(answer_len=0).values('qa_id','question', 'description', 'answer_len', 'views', 'user__first_name', 'code','created_at')
    
    else:
        questions = models.Qa.objects.all().values('qa_id','question', 'description', 'answer_len', 'views', 'user__first_name', 'code','created_at')

    length = len(questions)
    if page+1 < length/5:
        start = page * 5
        end = start + 5
        page = int(end/5)
        questions = questions[start:end]

    else:
        status = False
        remaining = length % 5 if length % 5 != 0 else 5
        questions = questions[length - remaining:]
        page = page + 1

    questions = list(questions)
    for question in questions:
        question['courses'] = []
        quiz = models.Qa.objects.get(qa_id=question['qa_id'])
        courses = list(models.Question_subjects.objects.filter(question=quiz).values('course__course_name'))
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
                subject = models.Question_subjects(course=course, question=question)
                subject.save()


        for key, img in images:
            title = uuid.uuid4()
            ext = os.path.splitext(img.name)[1]
            img.name = f'{title}.{ext}'
            image = models.Images.objects.create(title = title, file=img)
            image.save()
            image_ref = models.Image_reference.objects.create(question=question, image=image)
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
        return render(request, 'QuestionAnswer/question_form.html', context)

def Question(request, id):
    question = get_object_or_404(models.Qa, code=id)
    User = get_user_model()
    user = User.objects.get(id=question.user.id)
    courses = models.Question_subjects.objects.filter(question=question)
    images_list = models.Image_reference.objects.filter(question=question)
    images = []
    if len(images_list) > 0:
        for img in images_list:
            images.append(img.image.file.url)
        

    question.views += 1
    question.save()
    
    user = models.AuthCustomuser.objects.get(id=question.user.id)
    if request.user.is_authenticated:
        me = models.AuthCustomuser.objects.get(id=request.user.id)
        rating = models.Ratings.objects.get(user=me, question=question).rating if len(models.Ratings.objects.filter(user=me, question=question)) > 0 else 0
    
    else:
        rating = 0
        ratings = models.Ratings.objects.filter(question=question)
        for rate in ratings:
            rating += rate.rating
        rating = rating/(len(ratings) if len(ratings) != 0 else 1)

    answers = models.Answers.objects.filter(question=question).order_by('-likes', '-created_at').values('answer', 'created_at', 'user__first_name', 'user__last_name', 'user__username', 'code', 'likes', 'user__image')

    for answer in answers:
        like = models.Likes.objects.filter(question=question, answer__code=answer['code'])
        if request.user.is_authenticated:
            answer['likes'] = [len(like), True if len(models.Likes.objects.filter(user=me, question=question, answer__code=answer['code'])) > 0 else False]
        else:
            answer['likes'] = len(like)
        
        answer['user__image'] = models.Images.objects.get(image_id=answer['user__image']) if answer['user__image'] != None else answer['user__image']
    
        answer['images'] = []
        images_list = models.Image_reference.objects.filter(answer__code=answer['code'])
        if len(images_list) > 0:
            for img in images_list:
                answer['images'].append(img.image.file.url)
    
    if request.user.is_authenticated:
        question_likes = [ len(models.Likes.objects.filter( question=question, answer=None)),True if len(models.Likes.objects.filter(user=me, question=question, answer=None)) > 0 else False]
    else:
        question_likes = len(models.Likes.objects.filter( question=question, answer=None))
    context = {
        'seeker':user,
        'id':id,
        'question':question,
        'courses' :courses,
        'images'  : images,
        'answers' : answers,
        'rating':rating,
        'likes' :question_likes

    }
    return render(request, 'QuestionAnswer/question_detail.html', context)

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

        answer = models.Answers.objects.create(user=user, question=question, answer=data['answer'], code=uuid.uuid4())
        answer.save()

        for key, img in imageset:
            title = uuid.uuid4()
            ext = os.path.splitext(img.name)[1]
            img.name = f'{title}.{ext}'
            image = models.Images.objects.create(title = title, file=img)
            image.save()

            image_ref = models.Image_reference.objects.create(answer=answer, question=question,image=image)
            image_ref.save()

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
        
        images_list = models.Image_reference.objects.filter(question=question)
        images = []
        if len(images_list) > 0:
            for img in images_list:
                images.append(img.image.file.url)
        
        context = {
            'question':question,
            'images'  : images,
            }
        return render(request, 'QuestionAnswer/answer.html', context)

def Vote(request):
    if request.method == 'POST' and request.user.is_authenticated:
        data = json.loads(request.body)
        id = data['id']
        Type = data['Type']

        context = {
            'status':True,
            'vote':0
            }

        user = models.AuthCustomuser.objects.get(id=request.user.id)
        if Type == 'question':
            question = models.Qa.objects.get(code=id)
            if len(models.Likes.objects.filter(user=user, question=question, answer=None)) > 0:
                like = models.Likes.objects.get(user=user, question=question, answer=None)
                like.likes += 1
                like.save()
            else:
                like = models.Likes(user=user, question=question, answer=None, likes=1)
                like.save()


            context['vote'] = like.likes

        elif Type == 'answer':
            question = models.Qa.objects.get(code=id)
            answer = models.Answers.objects.get(code=data['answer'])

            if len(models.Likes.objects.filter(user=user, question=question, answer=answer)) == 0:
                like = models.Likes(user=user, question=question, answer=answer, likes=1)
                like.save() 
                
                context['vote'] =  like.likes
        
        elif Type == 'rating':
            rating = int(data['rating'])
            question = models.Qa.objects.get(code=id)

            if len(models.Ratings.objects.filter(user=user, question=question)) > 0:
                rate = models.Ratings.objects.get(user=user, question=question)
                rate.rating = rating
                rate.save()
            else:
                rate = models.Ratings(user=user, rating=rating, question=question)
                rate.save()

        return JsonResponse(context)
    return JsonResponse({'status':False})