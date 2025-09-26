from django.db import models
from django.utils.translation import gettext_lazy as _

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

    class Meta:
        managed = False
        db_table = 'Auth_customuser'

class Market(models.Model):
    market_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(AuthCustomuser, models.DO_NOTHING, blank=True, null=True)
    title = models.CharField(max_length=200)
    slug = models.CharField(unique=True, max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.BooleanField(blank=True, null=True)
    amount = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'market'


class Notes(models.Model):
    note_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(AuthCustomuser, models.DO_NOTHING, blank=True, null=True)
    course = models.ForeignKey(Course, models.DO_NOTHING, blank=True, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    file_url = models.FileField(upload_to='Notes/')
    file_size = models.BigIntegerField(blank=True, null=True)
    views = models.IntegerField(blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    likes = models.IntegerField(blank=True, null=True)
    subjects = models.TextField(blank=True, null=True)  # This field type is a guess.
    pages = models.IntegerField(blank=True, null=True)
    uploaded_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'notes'


class Notifications(models.Model):
    notification_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(AuthCustomuser, models.DO_NOTHING, blank=True, null=True)
    message = models.TextField()
    is_read = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'notifications'

class Qa(models.Model):
    qa_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(AuthCustomuser, models.DO_NOTHING, blank=True, null=True)
    course = models.ForeignKey(Course, models.DO_NOTHING, blank=True, null=True)
    subjects = models.JSONField(blank=True, null=True)
    question = models.TextField()
    description = models.TextField(blank=True, null=True)
    answers = models.JSONField(blank=True, null=True)
    views = models.IntegerField(blank=True, null=True)
    likes = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'qa'

class StudyGroupMembers(models.Model):
    pk = models.CompositePrimaryKey('group_id', 'user_id')
    group = models.ForeignKey('StudyGroups', models.DO_NOTHING)
    user = models.ForeignKey(AuthCustomuser, models.DO_NOTHING)
    joined_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'study_group_members'
        unique_together = (('group', 'user'),)


class StudyGroups(models.Model):
    group_id = models.AutoField(primary_key=True)
    group_name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(AuthCustomuser, models.DO_NOTHING, db_column='created_by', blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'study_groups'
