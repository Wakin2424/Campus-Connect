from django.contrib import admin
from .models import *

# Register your models here.
class User_admin(admin.ModelAdmin):
    list_display = ['id', 'username','first_name', 'last_name', 'contact', 'email', 'is_active', 'graduation_level', 'year_of_study', 'career__career_name', 'course__course_name', 'date_joined',  'is_verified']

class career_admin(admin.ModelAdmin):
    list_display = ['career_id', 'career_name', 'description']

class Course_admin(admin.ModelAdmin):
    list_display = ['course_id', 'course_name', 'course_code', 'description']

class Market_admin(admin.ModelAdmin):
    list_display = ['market_id', 'user__first_name', 'title', 'slug', 'description', 'price', 'status', 'amount', 'created_at']

class Notes_admin(admin.ModelAdmin):
    list_display = ['note_id', 'user__first_name', 'course__course_name', 'title', 'description', 'file_size', 'views', 'rating', 'likes', 'subjects', 'pages', 'uploaded_at']

class Notification_admin(admin.ModelAdmin):
    list_display = ['notification_id', 'user__first_name', 'message', 'created_at']

class Qa_admin(admin.ModelAdmin):
    list_display = ['qa_id', 'user__first_name', 'course__course_name', 'views', 'likes', 'question', 'description', 'answers', 'created_at']

admin.site.register(Market, Market_admin)
admin.site.register(Qa, Qa_admin)
admin.site.register(Notifications, Notification_admin)
admin.site.register(Notes, Notes_admin)
admin.site.register(Course, Course_admin)
admin.site.register(Career, career_admin)
admin.site.register(CustomUser, User_admin)
