from django import forms
from .models import Product
from django.utils.html import strip_tags

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'thumbnail', 'category', 'is_featured', 'brand', 'stock', 'size']
        
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nama produk'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Harga produk'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Deskripsi produk',
                'rows': 4
            }),
            'thumbnail': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'URL gambar produk'
            }),
            'category': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Kategori produk'
            }),
            'brand': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Brand produk (opsional)'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Jumlah stok'
            }),
            'size': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ukuran (opsional)'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        
        labels = {
            'name': 'Nama Produk',
            'price': 'Harga (Rp)',
            'description': 'Deskripsi',
            'thumbnail': 'URL Gambar',
            'category': 'Kategori',
            'is_featured': 'Produk Unggulan',
            'brand': 'Brand',
            'stock': 'Stok',
            'size': 'Ukuran'
        }
 
    def clean_name(self):
        name = self.cleaned_data["name"]
        return strip_tags(name)
    
    def clean_price(self):
        price = self.cleaned_data["price"]
        return strip_tags(price)

    def clean_description(self):
        description = self.cleaned_data["description"]
        return strip_tags(description)
    
    def clean_thumbnail(self):
        thumbnail = self.cleaned_data["thumbnail"]
        return strip_tags(thumbnail)
    
    def clean_category(self):
        category = self.cleaned_data["category"]
        return strip_tags(category)
    
    def clean_brand(self):
        brand = self.cleaned_data.get("brand")
        if brand:
            return strip_tags(brand)
        return brand
    
    def clean_stock(self):
        stock = self.cleaned_data.get("stock")
        if stock:
            return strip_tags(stock)
        return stock
    
    def clean_size(self):
        size = self.cleaned_data.get("size")
        if size:
            return strip_tags(size)
        return size