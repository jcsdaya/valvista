from django import forms
from .models import Business, Category, Media

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        kwargs.setdefault("required", False)  # Allow empty uploads
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        if isinstance(data, (list, tuple)):
            result = [super().clean(d, initial) for d in data if d]
        else:
            result = [super().clean(data, initial)]
        return result

class BusinessForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
            queryset=Category.objects.all(),
            widget=forms.CheckboxSelectMultiple,
            required=True
    )
    photos = MultipleFileField()
    class Meta:
        model = Business
        fields = ['username','email','password','refid','name','location','description','categories' ,'time', 'timeclose', 'cost', 'photos', 'thumbnail','map']
       
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'placeusername',
                'name': 'placeusername',
                'required': 'required',
                'placeholder': 'Enter Username (for login)'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'id': 'placeemail',
                'name': 'placeemail',
                'required': 'required',
                'placeholder': 'Enter Email'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'id': 'placepass',
                'name': 'placepass',
                'required': 'required',
                'placeholder': 'Enter Password'
            }),
            'refid': forms.NumberInput(attrs={
                'class': 'form-control',
                'id': 'placeid',
                'name': 'placeid',
                'required': 'required',
                'placeholder': 'Enter Reference Number'
            }),
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
            'thumbnail': forms.ClearableFileInput(attrs={
                'class': 'custom-file-input',
                'id': 'placethumbnail',
                'name': 'placethumbnail'
            }),
            'map': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'placemap',
                'name': 'placemap',
                'placeholder': 'Enter map URL (Google Maps)'
            }),
       }
        
        
class BusinessUpdForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
            queryset=Category.objects.all(),
            widget=forms.CheckboxSelectMultiple,
            required=True
    )
    photos =  MultipleFileField()
    class Meta:
        model = Business
        fields = ['name','location','description','categories' ,'time', 'timeclose', 'cost', 'photos', 'thumbnail','map']
       
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
            'thumbnail': forms.ClearableFileInput(attrs={
                'class': 'custom-file-input',
                'id': 'placethumbnail',
                'name': 'placethumbnail'
            }),
            'map': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'placemap',
                'name': 'placemap',
                'placeholder': 'Enter map URL (Google Maps)'
            }),
       }