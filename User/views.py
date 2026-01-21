from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
import Auth.models as models


# Create your views here.
def Myprofile(request):
    if not request.user.is_authenticated:
        raise Http404('Invalid Request')
    
    user = models.AuthCustomuser.objects.get(id=request.user.id)
    
    questions = models.Qa.objects.filter(user=user).values('question', 'views', 'likes', 'code', 'created_at')
    notes = models.Notes.objects.filter(user=user).values('code', 'title', 'description', 'views', 'uploaded_at')
    products = models.Product.objects.filter(user=user)
    groups = models.GroupMember.objects.filter(user=user)

    total_uploads = len(questions) + len(notes)
    total_views = 0
    percentage = 0

    dict(user.__dict__)
    keys = ['username', 'first_name', 'last_name', 'email', 'contact', 'graduation_level', 'year_of_study', 'career_id', 'course_id', 'institution']
    for key in keys:
        if user.__dict__[key]:
            percentage += 1

    for question in questions:
        total_views += question['views']
    
    for note in notes:
        total_views += note['views']

    percentage = int((percentage / len(keys)) * 100)

    rating_sum = 0
    for rate in models.Ratings.objects.filter(user=user):
        rating_sum += rate.rating
    rate = len(models.Ratings.objects.filter(user=user))
    rating = [round(rating_sum/rate if rate != 0 else 1, 1) ,rate]

    context = {
        'notes': notes,
        'questions': questions,
        'products': products,
        'groups': groups,
        'percentage': percentage,
        'total_uploads':total_uploads,
        'total_views':total_views,
        'groups_joined': len(groups),
        'rating': rating,
    }
    return render(request, 'User/profile.html', context)

def Otherprofile(request, account):
    try:
        User = get_user_model()
        user = User.objects.get(username=account)
        user = models.AuthCustomuser.objects.get(username=account)
    except:
        raise Http404('There is no such account')
    
    notes = models.Notes.objects.filter(user=user).values('code', 'title', 'description', 'views', 'uploaded_at')
    questions = models.Qa.objects.filter(user=user).values('question', 'views', 'likes', 'code', 'created_at')
    products = models.Product.objects.filter(user=user)
    groups = models.GroupMember.objects.filter(user=user)

    context = {
        'account':user,
        'notes': notes,
        'products': products,
        'groups': groups,
        'questions': questions,
        'total_uploads': questions,
        'groups_joined': len(groups),
    }
    return render(request, 'User/user.html', context)
