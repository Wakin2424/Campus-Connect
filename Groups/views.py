from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from Auth import models
from django.http import HttpResponse, JsonResponse
import uuid
import datetime
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count, Q

# Create your views here.
@login_required
def groupCreateRender(request):
    if request.method == 'POST':
        print(request.POST)
        group_name = request.POST.get('group-name')
        group_desc = request.POST.get('group-description')
        form_course = request.POST.get('group-course')
        group_privacy = request.POST.get('privacy') == 'on'

        form_img = request.FILES.get('group-image')
        group_image = models.Images.objects.create(title = uuid.uuid4(), file=form_img)
        group_course = models.Course.objects.get(course_id=form_course)

        slug = group_name.lower().replace(' ', '-')
        slug += '-' + str(models.Group.objects.filter(slug__startswith=slug).count() + 1)

        try:
            user = models.AuthCustomuser.objects.get(id=request.user.id)
        
            group = models.Group.objects.create(
                name=group_name,
                description=group_desc,
                course=group_course,
                is_private=group_privacy,
                slug=slug,
                admin = user,
                image=group_image
            )

            group_member = models.GroupMember.objects.create(
                group=group,
                user=user,
                role='admin'
            )

            data = {
                'user_first_name': request.user.first_name,
                'username':request.user.username,
                'message': "Welcome to the group chat!",
                'image_url': user.image.file.url if user.image != None else None,
                'timestamp': f'{datetime.datetime.now().isoformat()}',
                'ai': False
            }

            group_messages = models.GroupMessages.objects.create(
                group=group,
                messages=[data],
                msg_index=1
                )


            url = request.build_absolute_uri(reverse('group_detail', kwargs={'group': group.slug}))
            return JsonResponse({'status': True, 'url': url})
        except Exception as e:
            print(e)
            return JsonResponse({'status': False})
        
    courses = models.Course.objects.all().order_by('course_name')
    context = {
        'courses': courses
    }
    return render(request, 'Groups/create-group.html', context)
    
def groupHomeRender(request):
    groups = models.Group.objects.all().order_by('members_no')[:6]
    #categories = models.Group.course.all()[:6]

    context = {
        'groups': groups,
        'category': []
    }
    return render(request, 'Groups/group-landing-page.html', context)

def groupDetailRender(request, group):
    group = get_object_or_404(models.Group, slug=group)
    members = models.GroupMember.objects.filter(group=group)
    is_member = False

    if request.user.is_authenticated:
        user = models.AuthCustomuser.objects.get(id=request.user.id)

        if members.filter(user=user).exists():
            is_member = True
    
    context = {
        'group' : group,
        'members' : members,
        'is_member' : is_member
    }

    return render(request, 'Groups/group-detail.html', context)

@login_required
def joinGroup(request, group):
    group = get_object_or_404(models.Group, slug=group)
    user = models.AuthCustomuser.objects.get(id=request.user.id)
    models.GroupMember.objects.create(group=group, user=user, role='member')
    url = request.build_absolute_uri(reverse('group_detail', kwargs={'group': group.slug}))
    return redirect(url)

def chatRoomRender(request, group):
    group = get_object_or_404(models.Group, slug=group)
    messages = models.GroupMessages.objects.get(group=group)
    members = len(models.GroupMember.objects.filter(group=group))

    context = {
        'group' : group,
        'members' : members,
        'messages' : messages
    }

    return render(request, 'Groups/chat-room.html', context)

def GetGroupsApi(request):
    """
    API endpoint to get paginated list of groups.
    Returns groups with member counts and pagination metadata.
    """
    try:
        results = {}

        page = int(request.GET.get('page')) if request.GET.get('page') != None else 1

        groups = models.Group.objects.all()[:6].values('group_id', 'name', 'description', 'image__file__url', 'members_no')
        groups = list(groups)
        
        results['results'] = groups
        results['count'] = len(groups)

        if page <= 1:
            results['previous'] = False
        else:
            results['previous'] = True

        if results['count'] >= 6:
            results['next'] = True
        else:
            results['next'] = False

        return JsonResponse(results)
    
    except Exception as e:
        print(e)
        return JsonResponse({'error': str(e)}, status=500)
    

"""
{
  "count": 120,
  "next": "http://localhost:8000/api/groups/?page=2&page_size=6",
  "previous": null,
  "results": [
    {
      "group_id": 1,
      "name": "Machine Learning Students",
      "description": "Discussion and collaboration for ML students.",
      "group_image": "/media/groups/ml.jpg",
      "members_count": 145
    },
    {
      "group_id": 2,
      "name": "Web Development 2024",
      "description": "Learn HTML, CSS, JavaScript, React",
      "group_image": "/media/groups/webdev.jpg",
      "members_count": 89
    }
  ]
}
"""
