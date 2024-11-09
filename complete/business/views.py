from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import BusinessForm
from django.contrib.auth.models import Group
from .models import Business,Media
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from website.models import Notification


def login_business(request):
    if request.method =="POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.success(request,("There is an error logging in, try again."))
            return redirect('login_business')
        
    else:
        return render(request,'authentication/login.html',{})    
    
def logout_business(request):
     logout(request)
     messages.success(request,("You were Logged Out!"))
     return redirect('home')
     

def register_business(request):
    form = BusinessForm()
    if request.POST:
        form = BusinessForm(request.POST, request.FILES)
        if form.is_valid():
            # Save business form data
            business = form.save(commit=False)
            business.save()

            # Setting categories field separately
            form.instance.categories.set(form.cleaned_data['categories'])

            # Handle the uploaded photos
            photos = request.FILES.getlist('photo')
            for photo in photos:
                photo_instance = Media(file=photo)
                photo_instance.save()
                business.photo.add(photo_instance)

            business.save()


            admin_group = Group.objects.get(name='Admin') 
            users= admin_group.user_set.all() 
            for user in users:
                Notification.objects.create(
                    user=user,
                    message=f"A new business '{business.name}' has been registered.",
                    placeid=business.id,
                    origin = "register_business"
                )


            return redirect('login')
    
    return render(request, 'authentication/register_business.html', {'form': form})

  
