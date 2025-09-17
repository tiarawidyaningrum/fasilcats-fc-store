from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core import serializers
from .models import Product
from .forms import ProductForm

def show_main(request):
    # Ambil data product dari database
    products = Product.objects.all()

    # Data untuk template
    context = {
        'app_name': 'Fasilcats FC Store',
        'name': 'Tiara Widyaningrum',
        'class': 'PBP D',
        'description': 'Toko official Fasilcats FC yang menyediakan berbagai merchandise sepak bola.',
        'tagline': 'Viva Viva Fasilkom!',
        'identity': 'Made with ❤️ by Tiara Widyaningrum - Fasilkom UI Student | PBP D 2025',
        'products': products
    }
    
    return render(request, 'main.html', context)

def create_product(request):
    form = ProductForm(request.POST or None)
    
    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('main:show_main'))
    
    context = {'form': form}
    return render(request, "create_product.html", context)

def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    context = {'product': product}
    return render(request, 'product_detail.html', context)

# data delivery
def show_xml(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")