from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import BusinessForm
from .models import Business
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden


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
     


@login_required
def register_business(request):
    if not request.user.groups.filter(name='Business').exists():
        return HttpResponseForbidden("You don't have permission to access this page.")
    if request.POST:
        form = BusinessForm(request.POST, request.FILES)
        if form.is_valid():
            business_details = form.save(commit=False)
            business_owner = Business.objects.get(username=request.user.username)
            business_details.businessowner = business_owner
            business_details.save()
        return redirect('businesslist')
    else:
        form = BusinessForm()
    return render(request, 'authentication/register_business.html',{'form':form})

  
