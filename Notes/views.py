from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponse, JsonResponse
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.views.decorators.clickjacking import xframe_options_sameorigin
import json, os, uuid
import datetime as dt
from Auth import models
import os, mimetypes
from io import BytesIO
import uuid
from PyPDF2 import PdfReader
from docx import Document
from docx2pdf import convert

def get_uploaded_file_metadata(uploaded_file):
    metadata = {
        "name": uploaded_file.name,
        "size_kb": round(uploaded_file.size / 1024, 2),
        "type": uploaded_file.content_type,
        "pages":1
    }

    try:
        if uploaded_file.name.lower().endswith(".pdf"):
            reader = PdfReader(uploaded_file)
            metadata["pages"] = len(reader.pages)

        elif uploaded_file.name.lower().endswith(".docx"):
            doc = Document(uploaded_file)
            uploaded_file = convert(uploaded_file)
            reader = PdfReader(uploaded_file)
            metadata["pages"] = len(reader.pages)
    except Exception as e:
        metadata["pages"] = 1

    return metadata

# Create your views here.
def Home(request):
    courses = models.Course.objects.all()
    context = {
        'courses':courses
    }
    return render(request, 'Notes/notes.html', context)

def LoadHomeData(request):
    page = int(request.GET.get('page'))
    Type = request.GET.get('request')
    course_request = request.GET.get('course')
    status = True

    if Type == 'downloads':
        notes = models.Notes.objects.all().order_by('downloads').values('note_id', 'code', 'user__first_name', 'user__last_name', 'title', 'description', 'views', 'downloads', 'uploaded_at')
    else:
        notes = models.Notes.objects.all().values('note_id', 'code', 'user__first_name', 'user__last_name', 'title', 'description', 'views', 'downloads', 'uploaded_at')

    if course_request != None and course_request != 'All Courses':
        tag = request.GET.get('course')
        course = models.Course.objects.get(course_name=tag)
        notes = notes.filter(courses=course).values('note_id', 'code', 'user__first_name', 'user__last_name', 'title', 'description', 'views', 'downloads', 'uploaded_at')

    length = len(notes)
    if length != 0:
        if page+1 < length/5:
            start = page * 5
            end = start + 5
            page = int(end/5)
            notes = notes[start:end]

        else:
            status = False
            remaining = length % 5 if length % 5 != 0 else 5
            notes = notes[length - remaining:]
            page = page + 1

        notes = list(notes)
        for note in notes:
            note['courses'] = []
            note_data = models.Notes.objects.get(note_id=note['note_id'])
            courses = list(models.Question_subjects.objects.filter(note=note_data).values('course__course_name'))
            for course in courses:
                note['courses'].append(course['course__course_name'])

            del note['note_id']
    else:
        status = False
        notes = None
    
    context = {
        'status':status,
        'page':page,
        'notes':notes
    }
    return JsonResponse(context)

def GetAllCourses(request):
    """
    Returns a list of all courses with optional search functionality.
    """
    try:
        # Get search parameter if provided
        search_query = request.GET.get('search', None)
        
        # Base queryset
        courses_qs = models.Course.objects.all()
        
        # Apply search filter if provided
        if search_query:
            courses_qs = courses_qs.filter(
                course_name__icontains=search_query
            )
        
        # Order by name
        courses_qs = courses_qs.order_by('course_name')
        
        # Get values
        courses = courses_qs.values(
            'course_id', 
            'course_name'
        )
        
        courses_list = list(courses)
        
        context = {
            'status': True,
            'count': len(courses_list),
            'courses': courses_list
        }
        
        return JsonResponse(context, safe=False)
        
    except Exception as e:
        return JsonResponse({
            'status': False,
            'error': str(e),
            'courses': []
        }, status=500)

@xframe_options_sameorigin
def Note_Detail(request, id):
    note = get_object_or_404(models.Notes, code=id)
    note.views += 1
    note.save()
    ratings = models.Ratings.objects.filter(note=note)
    rating = 0
    rating_len =  len(ratings)
    for i in ratings:
        rating += i.rating
    
    rating = round(rating/rating_len, 1) if rating_len != 0 else 0
    size = round(note.file_size/1024, 2)
    likes = [len(models.Likes.objects.filter(note=note)), False]
    courses = models.Question_subjects.objects.filter(note=note)
    
    related_notes = []

    context = {
        'note':note,
        'related_notes': related_notes,
        'rating':rating,
        'size':size,
        'likes':likes,
        'courses':courses
    }
    return render(request, 'Notes/notes_details.html', context)

@xframe_options_sameorigin
def notesDetailsApi(request, id):
    """
    API endpoint to get note details in JSON format.
    Similar to Note_Detail but returns JSON instead of HTML.
    """
    try:
        # Get the note or return 404
        note = get_object_or_404(models.Notes, code=id)
        
        # Increment view count
        note.views += 1
        note.save()
        
        # Calculate rating
        ratings = models.Ratings.objects.filter(note=note)
        rating = 0
        rating_len = len(ratings)
        for i in ratings:
            rating += i.rating
        
        rating = round(rating / rating_len, 1) if rating_len != 0 else 0
        
        # Calculate file size in KB
        size = round(note.file_size / 1024, 2) if note.file_size else 0
        
        # Handle likes based on authentication
        if request.user.is_authenticated:
            likes_count = len(models.Likes.objects.filter(note=note))
            user_liked = len(models.Likes.objects.filter(user=request.user, note=note)) > 0
            likes = [likes_count, user_liked]
        else:
            likes = [len(models.Likes.objects.filter(note=note)), False]
        
        # Get courses for this note
        courses = models.Question_subjects.objects.filter(note=note).values(
            'course__course_id', 
            'course__course_name'
        )
        courses_list = list(courses)
        
        # Get related notes (example: same courses)
        related_notes_list = []
        if courses_list:
            # Get course IDs
            course_ids = [course['course__course_id'] for course in courses_list]
            
            # Find notes with same courses, excluding current note
            related_notes_qs = models.Notes.objects.filter(
                question_subjects__course__course_id__in=course_ids
            ).exclude(
                code=note.code
            ).distinct().values(
                'note_id', 'code', 'title', 'description', 
                'views', 'downloads', 'uploaded_at',
                'user__first_name', 'user__last_name'
            )[:5]  # Limit to 5 related notes
            print(note)
            related_notes_list = list(related_notes_qs)
            
            # Format datetime fields
            for related_note in related_notes_list:
                if related_note.get('uploaded_at'):
                    related_note['uploaded_at'] = related_note['uploaded_at'].isoformat()
        
        # Get user who uploaded the note
        user_data = {
            'id': note.user.id,
            'first_name': note.user.first_name,
            'last_name': note.user.last_name,
            'username': note.user.username,
            'email': note.user.email if hasattr(note.user, 'email') else None,
        }
        
        
        # Get note images if any
        images = []
    
        # Prepare response data
        context = {
            'status': True,
            'note': {
                'code': note.code,
                'title': note.title,
                'description': note.description,
                'views': note.views,
                'downloads': note.downloads,
                'file_size': size,  # Size in KB
                'file_url': note.file_url.url if note.file_url else None,
                'filename': f"{note.title}",
                'created_at': note.uploaded_at.isoformat() if note.uploaded_at else None,
                'user': user_data
            },
            'related_notes': related_notes_list,
            'rating': rating,
            'rating_count': rating_len,
            'size': size,
            'likes': likes,
            'courses': courses_list,
            'images': images
        }
        
        return JsonResponse(context, safe=False)
        
    except Exception as e:
        print(e)
        return JsonResponse({
            'status': False,
            'error': str(e)
        }, status=500)

def Note_Upload(request):
    if request.method == 'POST':
        context = {
            'status' : True
        }

        try:
            # POST data
            dataset = request.POST.copy()
            file = request.FILES['file']
            context['status'] = True

            if file.size/pow(1024, 2) > 30:
                raise Exception("File exceeds 30 MB limit!")
            
            user = models.AuthCustomuser.objects.get(id=request.user.id)
            code = uuid.uuid4()
            file_type = str(file.name).split('.')[1]
            file.name = f"{code}.{file_type}"
            pages = get_uploaded_file_metadata(file)['pages']

            note = models.Notes.objects.create(user=user, code=code, title=dataset['title'], description=dataset['description'], file_url=file, file_size=file.size/1024, file_type=file_type, views=0, pages=pages)

            for courseData in dataset['courses']:
                if len(models.Course.objects.filter(course_name=courseData)) > 0:
                    course = models.Course.objects.get(course_name=courseData)
                    subject = models.Question_subjects(course=course, note=note)
                    subject.save()

            context['url'] = f'{request.build_absolute_uri("note")}/{code}/'
        except Exception as e:
            context['status'] = False
            context['error'] = str(e)
        
        return JsonResponse(context)
    
    else:
        courses = models.Course.objects.all().values('course_name')

        context = {
            'courses':courses
        }
        return render(request, 'Notes/upload_notes.html', context)