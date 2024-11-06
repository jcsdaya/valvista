from django import forms
from .models import Business, Category, Media,Rating
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

class BusinessForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
            queryset=Category.objects.all(),
            widget=forms.CheckboxSelectMultiple,
            required=True
    )
    photos = MultipleFileField()
    class Meta:
        model = Business
        fields = ['username','email','password','refid','name','location','description','categories' ,'time', 'timeclose', 'cost', 'photos', 'thumbnail','map','status','lat','lng']
       
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
            'status': forms.Select(attrs={
                'class': 'form-control',
                'id': 'placestatus',
                'name': 'placestatus',
                'placeholder': 'Enter status'
            }),
       }
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Business.objects.filter(email=email).exists():  # Adjust for your model
            raise ValidationError("This email is already registered.")
        if not (email.endswith('@gmail.com') or email.endswith('@yahoo.com')):
            raise ValidationError("Email must be a valid Gmail or Yahoo address.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if Business.objects.filter(username=username).exists():  # Adjust for your model
            raise ValidationError("This username is already taken.")
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 8 or not any(char.isdigit() for char in password):
            raise ValidationError("Password must be at least 8 characters long and contain at least one number.")
        return password
        
        
class BusinessUpdForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
            queryset=Category.objects.all(),
            widget=forms.CheckboxSelectMultiple,
            required=True
    )
    photos =  MultipleFileField()
    class Meta:
        model = Business
        fields = ['name','location','description','categories' ,'time', 'timeclose', 'cost', 'photos', 'thumbnail','map','status','lat','lng']
       
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
             'status': forms.Select(attrs={
                'class': 'form-control',
                'id': 'placestatus',
                'name': 'placestatus',
                'placeholder': 'Enter status'
            }),
       }

class BusinessRating(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['name', 'score', 'comment']
    
    name = forms.CharField(max_length=100)
    score = forms.IntegerField(widget=forms.HiddenInput()) 
    comment = forms.CharField( widget=forms.Textarea(attrs={'rows': 8}), required=False)