from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model

# Create your views here.
def Login(request):
    if request.method == 'POST':
        user = authenticate(request, email=request.POST['email'], password=request.POST['password'])

        if user != None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'msg_bool':True, 'message':"Invalid Credentials"})
    else:
        return render(request, 'login.html')

def Signup(request):
    pass