from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser  # import your custom user model
from . import models

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    contact = forms.CharField(max_length=15, required=True)
    graduation_level = forms.CharField(required=False)
    year_of_study = forms.IntegerField(required=False)
    #career = forms.ChoiceField(required=False)
    #course = forms.ChoiceField(required=False)
    

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'email', 'contact', 'password1', 'password2', 'graduation_level', 'year_of_study', 'course', 'career')

       