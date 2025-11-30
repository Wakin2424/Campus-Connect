from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponse, JsonResponse
from django.contrib.auth import get_user_model
from django.db.models import Count
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
    return render(request, 'notes.html', context)

def LoadHomeData(request):
    page = int(request.GET.get('page'))
    Type = request.GET.get('request')
    course_request = request.GET.get('course')
    status = True

    if Type == 'downloads':
        notes = models.Notes.objects.all().order_by('downloads').values('note_id', 'code', 'user__first_name', 'user__last_name', 'title', 'description', 'views', 'downloads', 'uploaded_at')
    else:
        notes = models.Notes.objects.all().values('note_id', 'code', 'user__first_name', 'user__last_name', 'title', 'description', 'views', 'downloads', 'uploaded_at')

    if course_request != None:
        tag = request.GET.get('course')
        print(tag)
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
    print(size, note.file_size)
    context = {
        'note':note,
        'rating':rating,
        'size':size,
        'likes':likes,
        'courses':courses
    }
    return render(request, 'notes_details.html', context)

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
        return render(request, 'upload_notes.html', context)