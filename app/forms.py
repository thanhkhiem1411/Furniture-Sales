from django import forms
from django.forms import ModelForm
from .models import Product, Article

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

        labels = {
            'name': 'Tên sản phẩm',
            'price': 'Giá sản phẩm',
            'code': 'Mã sản phẩm',
            'digital': 'Sản phẩm số',
            'image': 'Hình ảnh sản phẩm',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập tên sản phẩm'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Nhập giá sản phẩm'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập mã sản phẩm'}),
            'digital': forms.Select(choices=[(True, 'Yes'), (False, 'No')], attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'placeholder': 'Chọn hình ảnh'}),
        }

class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = "__all__"

        labels = {
            'name': 'Tên bài viết',
            'image': 'Hình ảnh bài viết',
            'date_up': 'Ngày đăng',
            'content': 'Nội dung bài viết'
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập tên bài viết'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'placeholder': 'Chọn hình ảnh bài viết'}),
            'date_up': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Nhập ngày đăng'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Nhập nội dung bài viết'}),
        }