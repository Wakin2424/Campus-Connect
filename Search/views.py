from django.shortcuts import render
from Auth import models

# Create your views here.
def Search(request):
    result=request.GET['result']
    questions = models.Qa.objects.filter(question__icontains=result) | models.Qa.objects.filter(description__icontains=result)
    notes = models.Notes.objects.filter(title__icontains=result).values() | models.Notes.objects.filter(description__icontains=result).values()
    products = None

    if len(questions) == 0:
        questions = None

    if len(notes) > 0:
        for note in notes:
            courses = models.Question_subjects.objects.filter(note=models.Notes.objects.get(code=note['code']))
            if len(courses) == 0:
                note['courses'] = None
            else:
                note['courses'] = courses
    else:
        notes = None

    context = {
        'result':result,
        'questions': questions, 
        'notes':notes,
        'products':products
    }
    return render(request, 'search.html', context)
