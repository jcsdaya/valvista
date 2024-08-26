from django import forms
from .models import Place
from .models import NormalUser,Rating
from business.models import Business
from django import forms
from .models import Place

class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = [
            'name', 'location', 'description', 'category', 'category2',
            'category3', 'time', 'timeclose', 'cost', 'photo', 'photos',
            'thumbnail', 'map','promos','announcement'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'placename',
                'name': 'placename',
                'required': 'required',
                'placeholder': 'Enter place name'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'placelocation',
                'name': 'placelocation',
                'placeholder': 'Enter location'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'placedescription',
                'name': 'placedescription',
                'rows': 3
            }),
            'category': forms.Select(attrs={
                'class': 'form-control',
                'id': 'placecategory',
                'name': 'placecategory'
            }),
            'category2': forms.Select(attrs={
                'class': 'form-control',
                'id': 'placecategory2',
                'name': 'placecategory2'
            }),
            'category3': forms.Select(attrs={
                'class': 'form-control',
                'id': 'placecategory3',
                'name': 'placecategory3'
            }),
            'time': forms.TimeInput(attrs={
                'class': 'form-control',
                'id': 'placetime',
                'name': 'placetime',
                'placeholder': 'Enter opening time'
            }),
            'timeclose': forms.TimeInput(attrs={
                'class': 'form-control',
                'id': 'placetimeclose',
                'name': 'placetimeclose',
                'placeholder': 'Enter closing time'
            }),
            'cost': forms.Select(attrs={
                'class': 'form-control',
                'id': 'placecost',
                'name': 'placecost',
                'placeholder': 'Enter cost'
            }),
            'photo': forms.ClearableFileInput(attrs={
                'class': 'custom-file-input',
                'id': 'placephoto',
                'name': 'placephoto'
            }),
            'photos': forms.ClearableFileInput(attrs={
                'class': 'custom-file-input',
                'id': 'placephotos',
                'name': 'placephotos'
            }),
            'thumbnail': forms.ClearableFileInput(attrs={
                'class': 'custom-file-input',
                'id': 'placethumbnail',
                'name': 'placethumbnail'
            }),
            'map': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'placemap',
                'name': 'placemap',
                'placeholder': 'Enter map URL'
            }),
            'announcement': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'placeannouncement',
                'name': 'placeannouncement',
                'rows': 3
            }),
            'promos': forms.ClearableFileInput(attrs={
                'class': 'custom-file-input',
                'id': 'placephoto',
                'name': 'placephoto'
            }),
            
        }


        
class SignupForm(forms.ModelForm):
    class Meta:
        model = NormalUser
        fields = ['username', 'email', 'password']


class BusinessRegForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ['username','password','email','refid']

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['score', 'comment']
        widgets = {
            'score': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }


