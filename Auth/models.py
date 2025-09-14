from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime as dt
from django.utils.translation import gettext_lazy as _

# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    contact = models.CharField(max_length=15, blank=True)
    course_id = models.ForeignKey('course')
    career_id = models.ForeignKey('')
    

    USERNAME_FIELD = 'email'         # Use email to log in
    REQUIRED_FIELDS = ['username']   # Required when creating superuser

    def __str__(self):
        return self.email