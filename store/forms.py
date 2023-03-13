from dataclasses import fields
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Image, Order, Review

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['file', 'fb_link', 'image_id', 'is_text', 'text', 'text_size', 'text_font', 'text_color']


class MoonImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('file', 'is_text')

class MoonImageEditForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('text', 'text_font', 'text_color')

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('status',)

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields =  ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'rows':1, 'cols':50, 'id':'text', 'class':'form-control', 'placeHolder': 'write your review here'}),
        }
        
class SearchForm(forms.Form):
    search_query = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'placeholder': 'חפש הזמנה..'}))