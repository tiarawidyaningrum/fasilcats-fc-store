from django import forms
from .models import Product

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