from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from . import form as Form
from . import models
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