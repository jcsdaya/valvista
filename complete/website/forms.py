from django import forms
from .models import Place
from .models import NormalUser,Rating
from business.models import Business
from django import forms
from .models import Place,Category
from django.core.exceptions import ValidationError

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

class PlaceForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    photo = MultipleFileField()
    class Meta:
        model = Place
        fields = [
            'name', 'location', 'description', 'categories', 'time', 'timeclose', 'cost', 'photo',
            'thumbnail', 'map','promos','announcement','status','lat','lng'
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
            'lat': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'placelat',
                'name': 'placelat',
                'placeholder': 'Enter latitude'
            }),
            'lng': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'placelng',
                'name': 'placelng',
                'placeholder': 'Enter longitude'
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
            'status': forms.Select(attrs={
                'class': 'form-control',
                'id': 'placestatus',
                'name': 'placestatus',
                'placeholder': 'Enter status'
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
        fields = ['email', 'username', 'password']  # Include other fields as necessary
        widgets = {
            'password': forms.PasswordInput(),  # Ensure password is not visible
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if NormalUser.objects.filter(email=email).exists():  # Adjust for your model
            raise ValidationError("This email is already registered.")
        if not (email.endswith('@gmail.com')):
            raise ValidationError("Email must be a valid Gmail address.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if NormalUser.objects.filter(username=username).exists():  # Adjust for your model
            raise ValidationError("This username is already taken.")
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 8 or not any(char.isdigit() for char in password):
            raise ValidationError("Password must be at least 8 characters long and contain at least one number.")
        return password
    


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['name', 'score', 'comment']
    
    name = forms.CharField(max_length=100,required=True)
    score = forms.IntegerField(widget=forms.HiddenInput(),required=True) 
    comment = forms.CharField( widget=forms.Textarea(attrs={'rows': 8}), required=False)

class PromoForm(forms.ModelForm):
 
 class Meta:
        model = Place
        fields = [
        'promos','announcement'
        ]
        widgets = {
 'announcement': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'placeannouncement',
                'name': 'placeannouncement',
                'rows': 8,
                'columns':10,
                'placeholder':'Enter Announcement here',
            }),
            'promos': forms.ClearableFileInput(attrs={
                'class': 'custom-file-input',
                'id': 'placephoto',
                'name': 'placephoto'
            }),
        }

class BusPromoForm(forms.ModelForm):
 
 class Meta:
        model = Business
        fields = [
        'promo','announcement'
        ]
        widgets = {
 'announcement': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'businessannouncement',
                'name': 'placeannouncement',
                'rows': 8,
                'columns':10,
                'placeholder':'Enter Announcement here',
            }),
            'promos': forms.ClearableFileInput(attrs={
                'class': 'custom-file-input',
                'id': 'placephoto',
                'name': 'placephoto'
            }),
        }

class NormalUserEditForm(forms.ModelForm):
    class Meta:
        model = NormalUser
        fields = ['email', 'password']

class BusinessEditForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ['email', 'password']