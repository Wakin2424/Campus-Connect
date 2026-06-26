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
from django.db.models import Count, Q, F
from rest_framework.decorators import api_view

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

    group.members_no += 1
    group.save()
    
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

        groups = models.Group.objects.annotate(id=F('slug'),group_image=F('image__file'),members_count=F('members_no')).values('id','name','description','group_image','members_count')[:6]
        groups = list(groups)
        
        for group in groups:
            if group['group_image']:
                group['group_image'] = f"/media/{group['group_image']}"

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

@api_view  
def joinGroupApi(request, group):
    if not request.user.is_authenticated:
        return JsonResponse({'status':False})
    
    try:
        group = get_object_or_404(models.Group, slug=group)
        user = models.AuthCustomuser.objects.get(id=request.user.id)
        models.GroupMember.objects.create(group=group, user=user, role='member')

        group.members_no += 1
        group.save()
        return JsonResponse({'status':True}, status=201)
    
    except:
        return JsonResponse({'status':False}, status=403)

@api_view(['GET'])
def groupDetailApi(request, group):
    """
    API endpoint to get group details in JSON format.
    Similar to groupDetailRender but returns JSON instead of HTML.
    """
    #try:
    # Get the group or return 404
    group = get_object_or_404(models.Group, slug=group)
    Dbmembers = models.GroupMember.objects.filter(group=group)
    members = []
    for Dbmember in Dbmembers:
        members.append({
            'user':{
                "first_name": Dbmember.user.first_name,
                "last_name": Dbmember.user.last_name,
                'email': Dbmember.user.email,
                "user_image": Dbmember.user.image.file.url if Dbmember.user.image != None else None,
            },
            'role': Dbmember.role,
            'joined_at':Dbmember.joined_at
        })

    is_member = None 

    if request.user.is_authenticated:
        is_member = Dbmembers.filter(user__email=request.user.email).exists()

    # Build response data
    context = {
        'id': group.slug,  # Using slug as identifier
        'group': {

            'name': group.name,
            'slug': group.slug,
            'description': group.description,
            'group_image': group.admin.image.file.url,
            'images': group.image.file.url,
            'members_count': group.members_no,
            'is_private': group.is_private,
            'created_at': group.created_at.isoformat() if group.created_at else None,
            'course': group.course.course_name,
            'admin':  {
                'id': group.admin.id,
                'first_name': group.admin.first_name,
                'last_name': group.admin.last_name,
                'username': group.admin.username,
                'email': group.admin.email if hasattr(group.admin, 'email') else None
            }
        },
        'is_member': is_member,
        'user_role': Dbmembers.get(user__email=request.user.email).role if is_member else None, # 'admin', 'member', or None
        'members': members,
        'members_count': len(Dbmembers),
    }
    
    return JsonResponse(context)
        
    """except Exception as e:
        print(e)
        return JsonResponse({
            'error': str(e),
            'status': False
        }, status=500)"""

