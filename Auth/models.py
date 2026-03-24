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

    def __str__(self):
        return f"{self.career_name}"

class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=150)
    course_code = models.CharField(unique=True, max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'course'
    
    def __str__(self):
        return f"{self.course_name}"

class Images(models.Model):
    image_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to="media/")

    class Meta:
        db_table = 'images'

    def __str__(self):
        return f"{self.title}"

class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    contact = models.CharField(max_length=15, blank=True)
    course = models.ForeignKey('course', null=True, blank=True, on_delete=models.SET_NULL, related_name='CUser')
    career = models.ForeignKey('career', null=True, blank=True, on_delete=models.SET_NULL, related_name='CUser')
    year_of_study = models.IntegerField(null=True, blank=True)
    graduation_level = models.CharField(max_length=200,  null=True, blank=True)
    institution = models.CharField(max_length=300, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    image = models.ForeignKey('Images', blank=True, null=True, on_delete=models.SET_NULL, related_name='CUser')
    

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
    career = models.ForeignKey('Career', blank=True, null=True, on_delete=models.SET_NULL, related_name='user')
    course = models.ForeignKey('Course', blank=True, null=True, on_delete=models.SET_NULL, related_name='user')
    image = models.ForeignKey('Images', blank=True, null=True, on_delete=models.SET_NULL, related_name='user')
    institution = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Auth_customuser'
    
    def __str__(self):
        return f"{self.first_name}"


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    slug = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'category'
    
    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(AuthCustomuser, on_delete=models.CASCADE, null=True, blank=True, related_name='product')
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product')
    courses = models.ManyToManyField(Course, through='Question_subjects')
    slug = models.CharField(max_length=200, unique=True)
    code = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    image = models.ForeignKey(Images, models.SET_NULL, null=True, related_name='product')
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'product'

    def __str__(self):
        return f"{self.user.first_name}: {self.name}"


class Notes(models.Model):
    note_id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=250, unique=True, default=uuid.uuid4())
    user = models.ForeignKey(AuthCustomuser, blank=True, null=True, on_delete=models.CASCADE, related_name='notes')
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
    
    def __str__(self):
        return f"{self.user.first_name}: {self.title}"


class Notifications(models.Model):
    notification_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(AuthCustomuser, blank=True, null=True, on_delete=models.CASCADE, related_name='notification')
    message = models.TextField()
    is_read = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True, default=str(dt.datetime.now()))

    class Meta:
        db_table = 'notifications'

class Qa(models.Model):
    qa_id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=250, unique=True)
    user = models.ForeignKey(AuthCustomuser, blank=True, null=True, on_delete=models.CASCADE, related_name='question')
    question = models.TextField()
    description = models.TextField(blank=True, null=True)
    views = models.IntegerField(blank=True, null=True, default=0)
    answer_len = models.IntegerField(default=0)
    created_at = models.DateTimeField(blank=True, default=str(dt.datetime.now()))
    courses = models.ManyToManyField(Course, through='Question_subjects')

    def __str__(self):
        return f"{self.user.first_name}: {self.question}"

    class Meta:
        db_table = 'qa'


class Answers(models.Model):
    answer_id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=250, unique=True)
    user = models.ForeignKey(AuthCustomuser, blank=True, null=True, on_delete=models.CASCADE, related_name='answer')
    question = models.ForeignKey('qa', blank=True, null=True, on_delete=models.CASCADE, related_name='answer')
    answer = models.TextField()
    ai = models.BooleanField(default=False)
    created_at = models.DateTimeField(blank=True, default=str(dt.datetime.now()))

    def __str__(self):
        return f"{self.user.first_name}: {self.answer}"

    class Meta:
        db_table = 'answers'

class Question_subjects(models.Model):
    reference_id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Qa, blank=True, null=True, on_delete=models.CASCADE, related_name='subject')
    note = models.ForeignKey(Notes, blank=True, null=True, on_delete=models.CASCADE, related_name='subject')
    course = models.ForeignKey(Course, blank=True, null=True, on_delete=models.CASCADE, related_name='subject')
    product = models.ForeignKey(Product, blank=True, null=True, on_delete=models.CASCADE, related_name='subject')

    class Meta:
        db_table = 'question_subjects'

class Image_reference(models.Model):
    reference_id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Qa, blank=True, null=True, on_delete=models.CASCADE, related_name='image_reference')
    answer = models.ForeignKey(Answers, blank=True, null=True, on_delete=models.CASCADE, related_name='image_reference')
    product = models.ForeignKey(Product, blank=True, null=True, on_delete=models.CASCADE, related_name='image_reference')
    image = models.ForeignKey(Images, on_delete=models.CASCADE)

    class Meta:
        db_table = 'image_reference'

class Ratings(models.Model):
    rating_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(AuthCustomuser, blank=True, null=True, on_delete=models.CASCADE, related_name='rating')
    rating = models.IntegerField(blank=True, null=True)
    question = models.ForeignKey(Qa, blank=True, null=True, on_delete=models.CASCADE, related_name='rating')
    note = models.ForeignKey(Notes, blank=True, null=True, on_delete=models.CASCADE, related_name='rating')
    product = models.ForeignKey(Product, blank=True, null=True, on_delete=models.CASCADE, related_name='rating')
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'ratings'


class Likes(models.Model):
    like_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(AuthCustomuser, blank=True, null=True, on_delete=models.CASCADE, related_name='likes')
    question = models.ForeignKey(Qa, blank=True, null=True, on_delete=models.CASCADE, related_name='likes')
    answer = models.ForeignKey(Answers, blank=True, null=True, on_delete=models.CASCADE, related_name='likes')
    note = models.ForeignKey(Notes, blank=True, null=True, on_delete=models.CASCADE, related_name='likes')
    likes = models.IntegerField(blank=True, null=True,default=0)
    created_at = models.DateTimeField(blank=True, null=True, default=str(dt.datetime.now()))
    class Meta:
        db_table = 'likes'
        unique_together = (('user', 'question', 'answer'))

class Address(models.Model):
    address_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(AuthCustomuser, blank=True, null=True, on_delete=models.CASCADE, related_name='address')
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    contact = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    class Meta:
        db_table = 'address'

    def __str__(self):
        return f"{self.user}: {self.address1}"

class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    transaction_id = models.CharField(unique=True, max_length=50)
    user = models.ForeignKey(AuthCustomuser, blank=True, null=True, on_delete=models.CASCADE, related_name='payment')
    product = models.ForeignKey('Product', blank=True, null=True, on_delete=models.SET_NULL, related_name='payment')
    payment_method = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.IntegerField(blank=True, null=True, default=1)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    class Meta:
        db_table = 'payment'
    
    def __str__(self):
        return f"{self.user.first_name} - {self.product.name}  {self.price}"

class Group(models.Model):
    group_id = models.AutoField(primary_key=True)
    admin = models.ForeignKey(AuthCustomuser,on_delete=models.CASCADE, related_name='group')
    name = models.CharField(max_length=200)
    slug = models.CharField(max_length=200, unique=True, default='')
    description = models.TextField(null=True, blank=True)
    course = models.ForeignKey(Course, blank=True, null=True, on_delete=models.SET_NULL, related_name='group')
    is_private = models.BooleanField(default=False)
    members_no = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ForeignKey('Images', blank=True, null=True, default=None, on_delete=models.SET_NULL, related_name='group')

    class Meta:
        db_table = 'groups'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class GroupMember(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('member', 'Member'),
    )

    member_id = models.AutoField(primary_key=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(AuthCustomuser, on_delete=models.CASCADE, related_name='group_memberships')
    role = models.CharField(max_length=10,choices=ROLE_CHOICES,default='member')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'group_members'
        unique_together = ('group', 'user')

    def __str__(self):
        return f"{self.user} - {self.group.name} ({self.role})"
    

class GroupMessages(models.Model):
    message_id = models.AutoField(primary_key=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_messages')
    msg_index = models.IntegerField(default=0)
    messages = models.JSONField(default=list)

    class Meta:
        db_table = 'group_messages'
    
    def __str__(self):
        return f"{self.group.name}: messages"