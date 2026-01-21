from django.shortcuts import render, get_object_or_404
from Auth import models

# Create your views here.
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
