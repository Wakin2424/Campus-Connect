from django.contrib import admin
from .models import *

# Register your models here.
class User_admin(admin.ModelAdmin):
    list_display = ['id', 'username','first_name', 'last_name', 'contact', 'email', 'is_active', 'graduation_level', 'year_of_study', 'career__career_name', 'course__course_name', 'date_joined', 'institution', 'image__title', 'is_verified']

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
    list_display = ['qa_id', 'code', 'user__first_name', 'answer_len', 'views', 'question', 'description', 'created_at']

class Question_subjects_admin(admin.ModelAdmin):
    list_display = ['reference_id', 'question__question', 'course__course_name']

class ImageReference_admin(admin.ModelAdmin):
    list_display = ['reference_id', 'question__question', 'image__title']

class Answer_admin(admin.ModelAdmin):
    list_display = ['answer_id', 'user__first_name', 'question__question', 'answer', 'created_at']

class Rating_admin(admin.ModelAdmin):
    list_display = ['rating_id', 'user__first_name', 'question__question', 'rating']

class Likes_admin(admin.ModelAdmin):
    list_display = ['like_id', 'user__first_name', 'question__question', 'answer__answer']

class Images_admin(admin.ModelAdmin):
    list_display = ['image_id', 'title', 'file']

admin.site.register(Market, Market_admin)
admin.site.register(Qa, Qa_admin)
admin.site.register(Notifications, Notification_admin)
admin.site.register(Notes, Notes_admin)
admin.site.register(Course, Course_admin)
admin.site.register(Career, career_admin)
admin.site.register(CustomUser, User_admin)
admin.site.register(Question_subjects, Question_subjects_admin)
admin.site.register(Image_reference, ImageReference_admin)
admin.site.register(Answers, Answer_admin)
admin.site.register(Ratings, Rating_admin)
admin.site.register(Likes, Likes_admin)
admin.site.register(Images, Images_admin)