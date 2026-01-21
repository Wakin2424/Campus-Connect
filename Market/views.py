from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import F
from django.urls import reverse
import Auth.models as models
import uuid, os

# Create your views here.
def Home(request):
    books = models.Product.objects.filter(category=models.Category.objects.get(slug='books'))[:3]
    notes = models.Product.objects.filter(category=models.Category.objects.get(slug='notes-and-handouts'))[:3]
    papers = models.Product.objects.filter(category=models.Category.objects.get(slug='articles'))[:3]
    study_guides = models.Product.objects.filter(category=models.Category.objects.get(slug='study-guides'))[:3]

   
    context = {
        'books':books,
        'notes':notes,
        'papers':papers,
        'study_guides':study_guides
    }
    return render(request, 'Market/market-landing-page.html', context)

def productLibrary(request):
    return render(request, 'Market/market.html')

def loadProducts(request):
    pass

def uploadProduct(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == "POST":
        if not request.user.is_authenticated:
            raise Http404("Invalid Request!")
    

        name = request.POST.get("name")
        category = request.POST.get("category")
        courses = request.POST.getlist("courses")
        description = request.POST.get('description')
        price = request.POST.get('price')
        discount = request.POST.get('discount')
        image_file = request.FILES.get("image")
        status = False

        try:
            if image_file != None:
                title = uuid.uuid4()
                ext = os.path.splitext(image_file.name)[1]
                image_file.name = f'{title}.{ext}'
                image = models.Images(title=title,file=image_file)
                image.save()
            else:
                image=None

            user = models.AuthCustomuser.objects.get(id=request.user.id)
            category = models.Category.objects.get(name=category)

            slug = str(name)
            slug = slug.replace(" ", "-")

            products = models.Product.objects.filter(slug=slug)
            if len(products) > 0 :
                slug = slug + f'{len(products) + 1}'

            product = models.Product(user=user, name=name, category=category, code=uuid.uuid4(), slug=slug, description=description, price=price, discount=discount, image=image)
            product.save()

            if image_file != None:
                image_ref = models.Image_reference(product=product, image=image)
                image_ref.save()

            for course_name in courses:
                course = models.Course.objects.get(course_name=course_name)
                subject = models.Question_subjects(product=product, course=course)
                subject.save()
            
            url = request.build_absolute_uri(reverse('product_detail', kwargs={'id': product.code}))
            status = True

            return JsonResponse({'status':status, 'url':url})

        except:
            return JsonResponse({'status':status})
                
    else:
        category = models.Category.objects.all()
        courses = models.Course.objects.all()
        context = {
            'categories' : category,
            'courses' : courses
        }
        return render(request, 'Market/product_upload.html', context)

def productDetail(request, id):
    product = get_object_or_404(models.Product, slug=id)
    category = models.Category.objects.get(category_id=product.category.category_id)
    User = get_user_model()
    seller = User.objects.get(id=product.user.id)
    courses = models.Question_subjects.objects.filter(product=product)
    related_products = list(models.Product.objects.filter(category=category)[:4])

    for index, related_product in enumerate(related_products):
        if related_product.product_id == product.product_id:
            related_products.pop(index)
            break

    context = {
        'product':product,
        'courses':courses,
        'seller':seller,
        'discount': round((product.price - product.discount)/product.price * 100, 0),
        'related_products':related_products

    }
    return render(request, 'Market/product_detail.html', context)

def updateProductDetail(request, id):
    if not request.user.is_authenticated:
        raise Http404('invalid request')
    
    product = get_object_or_404(models.Product, slug=id)

    if request.user.id != product.user.id:
        raise Http404('invalid request')

    negotiation_requests = models.Payment.objects.filter(payment_method='negotiate', status='pending').values(
        id=F('transaction_id'),
        user_name = F('user__first_name'),
        item = F('product__name'),
        requestedPrice = F('product__discount')
    )
    
    negotiation_requests = list(negotiation_requests)
    
    for index, negotiation_request in enumerate(negotiation_requests):
        negotiation_request['index'] = index+1

    context = {
        'product':product,
        'negotiation_requests': negotiation_requests,
    }

    return render(request, 'Market/edit-product.html', context)

def saveProductChanges(request):
    if request.method == 'POST':
        try:
            product = models.Product.objects.get(code=request.POST.get('id'))
            product.name = request.POST.get('name')
            product.description = request.POST.get('description')
            product.price = request.POST.get('price')
            product.discount = request.POST.get('discount')

            product.save()

            return JsonResponse({'status':True})
        except:
            return JsonResponse({'status':False})
    
        return
    return JsonResponse({'status':False})