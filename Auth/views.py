from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.core.cache import cache
from django.http import Http404
from django.urls import reverse
from . import form as Form
from . import models
import os, uuid

#
def getToken(user_id):
    token = uuid.uuid4().hex[:15].upper()
    cache.set(token, user_id, 500)
    return token

def authenticateToken(token):
    token = cache.get(token)
    return token

# Create your views here.
def Login(request):
    if request.method == 'POST':
        user = authenticate(request, email=request.POST['email'], password=request.POST['password'])

        if user != None:
            login(request, user)
            #previous_url = request.session.get('previous_url')
            #print(previous_url)

            #if previous_url != None:
            #    return redirect(previous_url)
            return redirect('home')
        else:
            return render(request, 'Auth/login.html', {'msg_bool':True, 'error':"Invalid Credentials"})
    else:
        previous_url = request.META.get('HTTP_REFERER') if request.META.get('HTTP_REFERER') != None else request.build_absolute_uri('home')
        #request.session['previous_url'] = previous_url

        return render(request, 'Auth/login.html', {'msg_bool':False})

def Logout(request):
    logout(request)
    return redirect('home')

def Signup(request):
    if request.method == 'POST':
        data = request.POST.copy()
        data['username'] = data['first_name'] + data['last_name']

        if data['career'] != '':
            if len(models.Career.objects.filter(career_name=data['career'])) > 0:
                data['career'] = models.Career.objects.get(career_name=data['career'])  
            else:
                career = models.Career(career_name=data['career'], description=data['career_description'])
                career.save()
                data['career'] = career

        if data['course'] != '':
            data['course'] = models.Course.objects.get(course_name=data['course']) if len(models.Course.objects.filter(course_name=data['course'])) > 0 else models.Course.objects.get(course_name='Other')
        
        print(data['career'])
        form = Form.CustomUserCreationForm(data)
        if form.is_valid():
            form.save()
            return redirect('login')

        careers = models.Career.objects.all().order_by('career_name')
        courses = models.Course.objects.all().order_by('course_name')
        context = {
            'careers': careers,
            'courses': courses,
            'error': form.error_messages
        }
        return render(request, 'Auth/signup.html', context)

    else:
        careers = models.Career.objects.all().order_by('career_name')
        courses = models.Course.objects.all().order_by('course_name')

        
        context = {
            'careers': careers,
            'courses': courses,
            'error': ''
        }
        return render(request, 'Auth/signup.html', context)
    
def EditProfile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == 'POST':
        data = request.POST.copy()
        img = request.FILES.get('pfp')

        data['username'] = str(data['first_name'] + data['last_name']).replace(' ', '')
        data['image'] = None

        if data['career'] != '':
            if len(models.Career.objects.filter(career_name=data['career'])) > 0:
                data['career'] = models.Career.objects.get(career_name=data['career'])  
            else:
                career = models.Career(career_name=data['career'], description=data['career_description'])
                career.save()
                data['career'] = career
        
        else:
            data['career'] = None

        if data['course'] != '':
            data['course'] = models.Course.objects.get(course_name=data['course']) if len(models.Course.objects.filter(course_name=data['course'])) > 0 else models.Course.objects.get(course_name='Other')
        else:
            data['course'] = None
        
        try:
            data['year_of_study'] = int(data['year_of_study'])

        except:
            data['year_of_study'] = None
        
        if img != None:
            if request.user.image == None:
                title = uuid.uuid4()
                ext = os.path.splitext(img.name)[1]
                img.name = f'{title}.{ext}'
                image = models.Images.objects.create(title = title, file=img)
                image.save()
            else:
                title = request.user.image.title
                request.user.image.file.delete()
                ext = os.path.splitext(img.name)[1]
                img.name = f'{title}.{ext}'
                image = models.Images.objects.get(title=title)
                print(image, image.title)
                image.file = img
                image.save()
        else:
            image = request.user.image

        data['image'] = image

        User = get_user_model()
        user = User.objects.get(id=request.user.id)
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.username = str(data['first_name'] + data['last_name']).replace(' ', '')
        user.email = data['email']
        user.contact = data['contact']
        user.graduation_level = data['graduation_level']
        user.year_of_study = data['year_of_study']
        user.career = data['career']
        user.course = data['course']
        user.institution = data['institution']
        user.image = data['image']
        
        del data['image']
        for key, value in data.items():
            if value == '' or value == None:
                user.is_verified = False
                break
            else:
                user.is_verified = True

        user.save()

        return redirect('user')

    
    else:
        careers = models.Career.objects.all().order_by('career_name')
        courses = models.Course.objects.all().order_by('course_name')

        
        context = {
            'careers': careers,
            'courses': courses,
            'error': ''
        }
        return render(request, 'Auth/edit_profile.html', context)

def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        User = get_user_model()
        user = User.objects.filter(email=email)
        
        if user.exists():
            user = user.first()

            from Mail.views import sendForgotPasswordURL
            
            token = getToken(user.pk)
            url = request.build_absolute_uri(reverse('reset_password', kwargs={'uidb64': str(uuid.uuid4()), 'token': token}))
            print(f"token: {token}, url:{url}")
            #django normal mail
            sendForgotPasswordURL(url, user.email, user.first_name)
            #celery mail
            #sendForgotPasswordURL.delay(url, user.email, user.first_name)

        return redirect('login')
        
    return render(request, 'Auth/forgot-password.html')

def resetPassword(request, uidb64, token):
    user_id = authenticateToken(token)
    
    if user_id == None:
        return redirect('reset_password_fail')
    
    if request.method == 'POST':
        new_password = request.POST.get('newPassword')

        if new_password == None:
            # redirect reset password error
            return redirect('reset_password_fail')

        User = get_user_model()

        user = User.objects.get(id=user_id)
        user.set_password(new_password)
        user.save()
        
        return redirect('reset_password_success')
    
    context = {
        'token' : token
    }
    return render(request, 'Auth/reset-password.html', context)

def resetPasswordSuccess(request):
    return render(request, 'Auth/password-reset-success.html')

def resetPasswordFailed(request):
    return render(request, 'Auth/password-reset-fail.html')
