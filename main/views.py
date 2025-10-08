from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.core import serializers
from .models import Product
from .forms import ProductForm
import json

@login_required(login_url='/login')
def show_main(request):
    # Ambil data product dari database
    filter_type = request.GET.get("filter", "my")

    if filter_type == "all":
        products = Product.objects.all()
    else:
        products = Product.objects.filter(user=request.user)

    print(f"Products count for {request.user.username}: {products.count()}")

    # Data untuk template
    context = {
        'app_name': 'Fasilcats FC Store',
        'name': request.user.username,
        'class': 'PBP D',
        'description': 'Toko official Fasilcats FC yang menyediakan berbagai merchandise sepak bola.',
        'tagline': 'Viva Viva Fasilkom!',
        'identity': 'Made with ❤️ by Tiara Widyaningrum - Fasilkom UI Student | PBP D 2025',
        'products': products,
        'last_login': request.COOKIES.get('last_login', 'Never')
    }
    
    return render(request, 'main.html', context)

@login_required(login_url='/login')
def create_product(request):
    print(f"User accessing create_product: {request.user.username}")
    form = ProductForm(request.POST or None)

    if request.method == "POST":
        print(f"POST data: {request.POST}")  

        if form.is_valid():
            product_entry = form.save(commit=False)
            product_entry.user = request.user
            product_entry.save()
            saved_product = Product.objects.get(id=product_entry.id)
            return HttpResponseRedirect(reverse('main:show_main'))
    
    context = {'form': form}
    return render(request, "create_product.html", context)

def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    context = {'product': product}
    return render(request, 'product_detail.html', context)

def edit_product(request, id):
    product = get_object_or_404(Product, pk=id)
    form = ProductForm(request.POST or None, instance=product)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_main') 

    context = {'form': form, 'product': product}
    return render(request, "edit_product.html", context)

def delete_product(request, id):
    product = get_object_or_404(Product, pk=id)
    product.delete()
    return HttpResponseRedirect(reverse('main:show_main'))

# Register, Login, Logout
def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form': form}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie('last_login', str(datetime.datetime.now().strftime('%d %b %Y at %H:%M:%S')))
            return response
    else:
        form = AuthenticationForm(request)
    context = {'form': form}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

# Data delivery
def show_xml(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    products = Product.objects.select_related('user').all()
    data = [
        {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'description': product.description,
            'thumbnail': product.thumbnail,
            'category': product.category,
            'is_featured': product.is_featured,
            'brand': product.brand,
            'stock': product.stock,
            'size': product.size,
            'created_at': product.created_at.isoformat() if product.created_at else None,
            'updated_at': product.updated_at.isoformat() if product.updated_at else None,
            'user_id': product.user_id,
            'user_username': product.user.username if product.user else None,
        }
        for product in products
    ]
    return JsonResponse(data, safe=False)

def show_xml_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    try:
        product = Product.objects.select_related('user').get(pk=id)
        data = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'description': product.description,
            'thumbnail': product.thumbnail,
            'category': product.category,
            'is_featured': product.is_featured,
            'brand': product.brand,
            'stock': product.stock,
            'size': product.size,
            'created_at': product.created_at.isoformat() if product.created_at else None,
            'updated_at': product.updated_at.isoformat() if product.updated_at else None,
            'user_id': product.user_id,
            'user_username': product.user.username if product.user else None,
        }
        return JsonResponse(data)
    except Product.DoesNotExist:
        return JsonResponse({'detail': 'Not found'}, status=404)

# AJAX

@csrf_exempt
@require_POST
@login_required(login_url='/login')
def add_product_ajax(request):
    name = strip_tags(request.POST.get("name"))
    price = request.POST.get("price")
    description = strip_tags(request.POST.get("description"))
    category = strip_tags(request.POST.get("category"))
    thumbnail = request.POST.get("thumbnail")
    brand = strip_tags(request.POST.get("brand")) if request.POST.get("brand") else None
    stock = request.POST.get("stock")
    size = strip_tags(request.POST.get("size")) if request.POST.get("size") else None
    is_featured = request.POST.get("is_featured") == 'on'
    user = request.user

    new_product = Product(
        name=name,
        price=price,
        description=description,
        category=category,
        thumbnail=thumbnail,
        brand=brand,
        stock=stock,
        size=size,
        is_featured=is_featured,
        user=user
    )
    new_product.save()

    return HttpResponse(b"CREATED", status=201)

@csrf_exempt
@require_POST
@login_required(login_url='/login')
def edit_product_ajax(request, id):
    product = get_object_or_404(Product, pk=id, user=request.user)
    
    product.name = strip_tags(request.POST.get("name"))
    product.price = request.POST.get("price")
    product.description = strip_tags(request.POST.get("description"))
    product.category = strip_tags(request.POST.get("category"))
    product.thumbnail = request.POST.get("thumbnail")
    product.brand = strip_tags(request.POST.get("brand")) if request.POST.get("brand") else None
    product.stock = request.POST.get("stock")
    product.size = strip_tags(request.POST.get("size")) if request.POST.get("size") else None
    product.is_featured = request.POST.get("is_featured") == 'on'
    
    product.save()

    return HttpResponse(b"UPDATED", status=200)

@csrf_exempt
@require_POST
@login_required(login_url='/login')
def delete_product_ajax(request, id):
    product = get_object_or_404(Product, pk=id, user=request.user)
    product.delete()
    return HttpResponse(b"DELETED", status=200)

# AJAX Authentication
@csrf_exempt
def register_ajax(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password1 = data.get('password1')
        password2 = data.get('password2')

        if password1 != password2:
            return JsonResponse({
                'status': False,
                'message': 'Passwords do not match.'
            }, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({
                'status': False,
                'message': 'Username already exists.'
            }, status=400)

        user = User.objects.create_user(username=username, password=password1)
        user.save()

        return JsonResponse({
            'status': True,
            'message': 'Account successfully created!'
        }, status=200)

    return JsonResponse({
        'status': False,
        'message': 'Invalid request method.'
    }, status=400)

@csrf_exempt
def login_ajax(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({
                'status': True,
                'message': 'Login successful!',
                'username': user.username
            }, status=200)
        else:
            return JsonResponse({
                'status': False,
                'message': 'Invalid username or password.'
            }, status=401)

    return JsonResponse({
        'status': False,
        'message': 'Invalid request method.'
    }, status=400)