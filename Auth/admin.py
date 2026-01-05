from django.contrib import admin
from .models import *

# Register your models here.
class User_admin(admin.ModelAdmin):
    list_display = ['id', 'username','first_name', 'last_name', 'contact', 'email', 'is_active', 'graduation_level', 'year_of_study', 'career__career_name', 'course__course_name', 'date_joined', 'institution', 'image__title', 'is_verified']

class career_admin(admin.ModelAdmin):
    list_display = ['career_id', 'career_name', 'description']

class Course_admin(admin.ModelAdmin):
    list_display = ['course_id', 'course_name', 'course_code', 'description']

class Notes_admin(admin.ModelAdmin):
    list_display = ['note_id', 'user__first_name', 'title', 'description', 'file_size', 'views', 'pages', 'uploaded_at']

class Notification_admin(admin.ModelAdmin):
    list_display = ['notification_id', 'user__first_name', 'message', 'created_at']

class Qa_admin(admin.ModelAdmin):
    list_display = ['qa_id', 'code', 'user__first_name', 'answer_len', 'views', 'question', 'description', 'created_at']

class Question_subjects_admin(admin.ModelAdmin):
    list_display = ['reference_id', 'question__question', 'note__title', 'course__course_name']

class ImageReference_admin(admin.ModelAdmin):
    list_display = ['reference_id', 'question__question', 'answer__answer', 'product__name', 'image__title']

class Answer_admin(admin.ModelAdmin):
    list_display = ['answer_id', 'user__first_name', 'question__question', 'answer', 'created_at']

class Category_admin(admin.ModelAdmin):
    list_display = ['category_id', 'name', 'slug', 'description', 'created_at']

class Product_admin(admin.ModelAdmin):
    list_display = ['product_id', 'user__first_name', 'name', 'category__name','slug', 'code', 'price', 'discount', 'status', 'created_at', 'description']

class Rating_admin(admin.ModelAdmin):
    list_display = ['rating_id', 'user__first_name', 'question__question', 'rating']

class Likes_admin(admin.ModelAdmin):
    list_display = ['like_id', 'user__first_name', 'question__question', 'answer__answer']

class Images_admin(admin.ModelAdmin):
    list_display = ['image_id', 'title', 'file']

class Payment_admin(admin.ModelAdmin):
    list_display = ['payment_id', 'transaction_id', 'user__first_name', 'product__name', 'payment_method', 'price', 'amount', 'status', 'created_at']

class Address_admin(admin.ModelAdmin):
    list_display = ['address_id', 'user__first_name', 'address1', 'address2', 'contact', 'city', 'postal_code', 'country', 'created_at']

class Group_admin(admin.ModelAdmin):
    list_display = ['group_id', 'admin__first_name', 'name', 'slug', 'description', 'course__course_name', 'is_private', 'created_at']

class GroupMembers_admin(admin.ModelAdmin):
    list_display = ['member_id', 'group__name', 'user__first_name','role', 'joined_at']

class GroupMessage_admin(admin.ModelAdmin):
    list_display = ['message_id', 'group__name', 'msg_index']

admin.site.register(Qa, Qa_admin)
admin.site.register(Notifications, Notification_admin)
admin.site.register(Notes, Notes_admin)
admin.site.register(Course, Course_admin)
admin.site.register(Career, career_admin)
admin.site.register(CustomUser, User_admin)
admin.site.register(Question_subjects, Question_subjects_admin)
admin.site.register(Image_reference, ImageReference_admin)
admin.site.register(Answers, Answer_admin)
admin.site.register(Category, Category_admin)
admin.site.register(Product, Product_admin)
admin.site.register(Ratings, Rating_admin)
admin.site.register(Likes, Likes_admin)
admin.site.register(Images, Images_admin)
admin.site.register(Payment, Payment_admin)
admin.site.register(Address, Address_admin)
admin.site.register(Group, Group_admin)
admin.site.register(GroupMember, GroupMembers_admin)
admin.site.register(GroupMessages, GroupMessage_admin)