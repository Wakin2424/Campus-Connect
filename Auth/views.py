from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.http import Http404
from . import form as Form
from . import models
import os, uuid
# Create your views here.
def Login(request):
    if request.method == 'POST':
        user = authenticate(request, email=request.POST['email'], password=request.POST['password'])

        if user != None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'msg_bool':True, 'error':"Invalid Credentials"})
    else:
        return render(request, 'login.html', {'msg_bool':False})

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
        return render(request, 'signup.html', context)

    else:
        careers = models.Career.objects.all().order_by('career_name')
        courses = models.Course.objects.all().order_by('course_name')

        
        context = {
            'careers': careers,
            'courses': courses,
            'error': ''
        }
        return render(request, 'signup.html', context)
    
def Edit(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == 'POST':
        data = request.POST.copy()
        img = request.FILES.get('pfp')
        print(request.FILES)

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
            else:
                title = request.user.image.title
                request.user.image.file.delete()

            ext = os.path.splitext(img.name)[1]
            img.name = f'{title}.{ext}'
            image = models.Images.objects.create(title = title, file=img)
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
        
        print(data)
        del data['image']
        for key, value in data.items():
            if value == '' or value == None:
                user.is_verified = False
                break
            else:
                user.is_verified = True

        user.save()

        return redirect('user')
    
        careers = models.Career.objects.all().order_by('career_name')
        courses = models.Course.objects.all().order_by('course_name')
        context = {
            'careers': careers,
            'courses': courses,
            'error': form.error_messages
        }
        return render(request, 'edit_profile.html', context)
    
    else:
        careers = models.Career.objects.all().order_by('career_name')
        courses = models.Course.objects.all().order_by('course_name')

        
        context = {
            'careers': careers,
            'courses': courses,
            'error': ''
        }
        return render(request, 'edit_profile.html', context)