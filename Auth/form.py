from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, CommerceCustomuser  # import your custom user model

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    contact = forms.CharField(max_length=15, required=True)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'email', 'contact', 'password1', 'password2')

       