from django import forms
from .models import Business

class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ['name','location','description','categories' ,'time', 'timeclose', 'cost', 'photo', 'photos', 'thumbnail','map','promo','announcement']
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
            'promo': forms.ClearableFileInput(attrs={
                'class': 'custom-file-input',
                'id': 'placephoto',
                'name': 'placephoto'
            }),
       }