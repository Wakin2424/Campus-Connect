from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime as dt
from django.utils.translation import gettext_lazy as _
import uuid

# Create your models here.
class Career(models.Model):
    career_id = models.AutoField(primary_key=True)
    career_name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'career'


class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=150)
    course_code = models.CharField(unique=True, max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'course'

class Images(models.Model):
    image_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to="media/")

    class Meta:
        db_table = 'images'

class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    contact = models.CharField(max_length=15, blank=True)
    course = models.ForeignKey('course', models.DO_NOTHING, null=True, blank=True)
    career = models.ForeignKey('career', models.DO_NOTHING, null=True, blank=True)
    year_of_study = models.IntegerField(null=True, blank=True)
    graduation_level = models.CharField(max_length=200,  null=True, blank=True)
    institution = models.CharField(max_length=300, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    image = models.ForeignKey('Images', models.DO_NOTHING, blank=True, null=True)
    

    USERNAME_FIELD = 'email'         # Use email to log in
    REQUIRED_FIELDS = ['username']   # Required when creating superuser

    def __str__(self):
        return self.email

class AuthCustomuser(models.Model):
    id = models.BigAutoField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    email = models.CharField(unique=True, max_length=254)
    contact = models.CharField(max_length=15)
    graduation_level = models.CharField(max_length=200, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    year_of_study = models.IntegerField(blank=True, null=True)
    career = models.ForeignKey('Career', models.DO_NOTHING, blank=True, null=True)
    course = models.ForeignKey('Course', models.DO_NOTHING, blank=True, null=True)
    image = models.ForeignKey('Images', models.DO_NOTHING, blank=True, null=True)
    institution = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Auth_customuser'


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    slug = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'category'


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(AuthCustomuser, on_delete=models.DO_NOTHING, null=True, blank=True)
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    courses = models.ManyToManyField(Course, through='Question_subjects')
    slug = models.CharField(max_length=200, unique=True)
    code = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    image = models.ForeignKey(Images, models.DO_NOTHING, null=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'product'


class Notes(models.Model):
    note_id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=250, unique=True, default=uuid.uuid4())
    user = models.ForeignKey(AuthCustomuser, models.DO_NOTHING, blank=True, null=True)
    courses = models.ManyToManyField(Course, through='Question_subjects')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    file_url = models.FileField(upload_to='Notes/')
    file_size = models.BigIntegerField(blank=True, null=True)
    file_type = models.CharField(max_length=10, default='.pdf')
    views = models.IntegerField(blank=True, null=True, default=0)
    pages = models.IntegerField(blank=True, null=True, default=1)
    downloads = models.IntegerField(blank=True, null=True, default=0)
    uploaded_at = models.DateTimeField(blank=True, null=True, default=str(dt.datetime.now()))

    class Meta:
        db_table = 'notes'


class Notifications(models.Model):
    notification_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(AuthCustomuser, models.DO_NOTHING, blank=True, null=True)
    message = models.TextField()
    is_read = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True, default=str(dt.datetime.now()))

    class Meta:
        db_table = 'notifications'

class Qa(models.Model):
    qa_id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=250, unique=True)
    user = models.ForeignKey(AuthCustomuser, models.DO_NOTHING, blank=True, null=True)
    question = models.TextField()
    description = models.TextField(blank=True, null=True)
    views = models.IntegerField(blank=True, null=True, default=0)
    answer_len = models.IntegerField(default=0)
    created_at = models.DateTimeField(blank=True, default=str(dt.datetime.now()))
    courses = models.ManyToManyField(Course, through='Question_subjects')

    class Meta:

        db_table = 'qa'

class Answers(models.Model):
    answer_id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=250, unique=True)
    user = models.ForeignKey(AuthCustomuser, models.DO_NOTHING, blank=True, null=True)
    question = models.ForeignKey('qa', models.DO_NOTHING, blank=True, null=True)
    answer = models.TextField()
    created_at = models.DateTimeField(blank=True, default=str(dt.datetime.now()))

    class Meta:
        db_table = 'answers'

class Question_subjects(models.Model):
    reference_id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Qa, models.DO_NOTHING, blank=True, null=True)
    note = models.ForeignKey(Notes, models.DO_NOTHING, blank=True, null=True)
    course = models.ForeignKey(Course, models.DO_NOTHING, blank=True, null=True)
    product = models.ForeignKey(Product, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'question_subjects'

class Image_reference(models.Model):
    reference_id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Qa, models.DO_NOTHING, blank=True, null=True)
    answer = models.ForeignKey(Answers, models.DO_NOTHING, blank=True, null=True)
    product = models.ForeignKey(Product, models.DO_NOTHING, blank=True, null=True)
    image = models.ForeignKey(Images, models.DO_NOTHING)

    class Meta:
        db_table = 'image_reference'

class Ratings(models.Model):
    rating_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(AuthCustomuser, models.DO_NOTHING, blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)
    question = models.ForeignKey(Qa, models.DO_NOTHING, blank=True, null=True)
    note = models.ForeignKey(Notes, models.DO_NOTHING, blank=True, null=True)
    product = models.ForeignKey(Product, models.DO_NOTHING, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'ratings'


class Likes(models.Model):
    like_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(AuthCustomuser, models.DO_NOTHING, blank=True, null=True)
    question = models.ForeignKey(Qa, models.DO_NOTHING, blank=True, null=True)
    answer = models.ForeignKey(Answers, models.DO_NOTHING, blank=True, null=True)
    note = models.ForeignKey(Notes, models.DO_NOTHING, blank=True, null=True)
    likes = models.IntegerField(blank=True, null=True,default=0)
    created_at = models.DateTimeField(blank=True, null=True, default=str(dt.datetime.now()))
    class Meta:
        db_table = 'likes'
        unique_together = (('user', 'question', 'answer'))