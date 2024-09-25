from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import SignupForm,PlaceForm,PromoForm,BusPromoForm
from business.forms import BusinessForm,BusinessUpdForm
from .models import Place,NormalUser,Visitor,Favorite,ItineraryState,PlaceMedia
from business.models import Business,Media
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User,Group
from django.http import HttpResponseForbidden
from .utils import get_home_context
from django.urls import reverse
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt




 
def home(request):
    
    context = get_home_context(request.user)
    return render(request, 'home.html', context)

def ratingform(request):
    
    return render(request, 'ratingform.html', {})


def add_favorite_place(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, place=place)
    if not created:
        favorite.delete()
    if request.get_full_path() == reverse('userhome'):
        return redirect('home')  
    else:
        return redirect('home')

def add_favorite_business(request, business_id):
    business = get_object_or_404(Business, id=business_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, business=business)
    if not created:
        favorite.delete()
    if request.get_full_path() == reverse('userhome'):
        return redirect('home')  
    else:
        return redirect('home')



def favorite_list(request):
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'favorite.html', {'favorites': favorites})
        

def loginuser(request):
    error_message=""
    if request.method =="POST":
        username = request.POST['username']
        password = request.POST['password']
        print(f"Username: {username}, Password: {password}")
        user = authenticate(request, username=username, password=password)
        print("User object type:", type(user))
        if user is not None:
            login(request, user)
            print(f"Authenticated User: {user}")
            if user.groups.filter(name='NormalUsers').exists():
                return redirect('home')
            elif user.groups.filter(name='Business').exists():
                business_user = Business.objects.get(username=username)
                if business_user.approval == True: 
                    return redirect('businesshome')
                else:
                    error_message = "Please wait as your account is on pending request"
                    return render(request,'login.html',{'error_message':error_message})
            else:
                return redirect('placelist')
        else:
            error_message = "Invalid username or password."
    return render(request,'login.html',{'error_message':error_message})

def logout_view(request):
    logout(request)
    return redirect('home')    

def register(request):
      if request.method == 'POST':
        form = SignupForm(request.POST or  None)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(username = form.cleaned_data['username'],password = form.cleaned_data['password'])
            login(request,new_user)
        return redirect('login')
      return render(request, 'register.html',{})
   
@login_required
def addplace(request):
    if not request.user.groups.filter(name='Admin').exists():
        return HttpResponseForbidden("You don't have permission to access this page.")
    form = PlaceForm()
    if request.POST:
        form = PlaceForm(request.POST, request.FILES)
        if form.is_valid():
            place = form.save(commit=False)
            place.save()
            print("Form cleaned data:", form.cleaned_data)
            form.instance.categories.set(form.cleaned_data['categories'])
            photo= request.FILES.getlist('photo')
            for photo in photo:
                photo_instance = PlaceMedia(file=photo)
                photo_instance.save()
                place.photo.add(photo_instance)
                place.save()
        return redirect('placelist')
    return render(request, 'addplace.html',{'form':form})

@login_required
def adminhome(request):
    if not request.user.groups.filter(name='Admin').exists():
        return HttpResponseForbidden("You don't have permission to access this page.")
    else:
       all_admin = Place.objects.all
       context = {'all_admin':all_admin}
       return render(request, 'adminhome.html',context)

@login_required
def userhome(request):
    if not request.user.groups.filter(name='NormalUsers').exists():
        return HttpResponseForbidden("You don't have permission to access this page.")
    else:
        context = get_home_context(request.user)
        return render(request, 'userhome.html',context)

@login_required
def businesshome(request):
    if not request.user.groups.filter(name='Business').exists():
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    # Fetch the Business instance related to the current user
    try:
        business = Business.objects.get(username=request.user.username)
    except Business.DoesNotExist:
        # Handle the case where the Business instance does not exist
        return HttpResponseForbidden("No associated business found.")
    
    if request.method == 'POST':
        form = BusPromoForm(request.POST, request.FILES, instance=business)
        if form.is_valid():
            form.save()
            return redirect('businesshome')
    else:
        form = BusPromoForm(instance=business)

    context = {'form': form}
    return render(request, 'businesshome.html', context)


@login_required
def viewrating(request,pk):
    if not request.user.groups.filter(name='Business').exists():
        return HttpResponseForbidden("You don't have permission to access this page.")
    else:
       business = get_object_or_404(Business, pk=pk)
       current_user_business = Business.objects.get(username=request.user.username)
       all_bus = Business.objects.filter(username=current_user_business)
       context = {'all_bus':all_bus,'business':business}
       return render(request, 'viewrating.html',context)

@login_required
def businesslist(request):
    excluded_groups = ['Business', 'Admin']
    if not any(request.user.groups.filter(name=group).exists() for group in excluded_groups):
        return HttpResponseForbidden("You don't have permission to access this page.")
    else:
        current_user_business = Business.objects.get(username=request.user.username)
        all_bus = Business.objects.filter(username=current_user_business)
        context = {'all_bus':all_bus}
        return render(request, 'businesslist.html',context) 

@login_required
def businessadmin(request):
    if not request.user.groups.filter(name='Admin').exists():
        return HttpResponseForbidden("You don't have permission to access this page.")
    else:
        all_buss = Business.objects.all
        context = {'all_buss':all_buss}
        return render(request, 'businessadmin.html',context) 
    

@login_required
def  admindelete(request,pk):
    if not request.user.groups.filter(name='Admin').exists():
        return HttpResponseForbidden("You don't have permission to access this page.")
    else:
        business = get_object_or_404(Business, pk=pk)
        if request.POST:
            business.archived = True
            business.save()     
            return redirect('businessadmin')
        context={'business':business}
        return render(request,'admindelete.html',context)
    
@login_required
def archives(request):
    if not request.user.groups.filter(name='Admin').exists():
        return HttpResponseForbidden("You don't have permission to access this page.")
    else:
        all_buss = Business.objects.all
        all_admin = Place.objects.all
        context = {'all_bus':all_buss,'all_admin':all_admin}
        return render(request, 'archives.html',context) 
    
@login_required
def dashboard(request):
    if not request.user.groups.filter(name='Admin').exists():
        return HttpResponseForbidden("You don't have permission to access this page.")
    else:
        previous_visits = Visitor.objects.filter(ip_address=request.META.get('REMOTE_ADDR', None), user_agent=request.META.get('HTTP_USER_AGENT', None))
        if previous_visits.exists():
                # User is accessing from the same device and IP, don't create a new Visitor object
                pass
        else:
                # User is accessing from a different device or IP, create a new Visitor object
                Visitor.objects.create(
                    ip_address=request.META.get('REMOTE_ADDR', None),
                    user_agent=request.META.get('HTTP_USER_AGENT', None),
                )
        all_businesses = Business.objects.all()
        all_users = NormalUser.objects.all()
        total_visitors = Visitor.objects.count()
        user_count = NormalUser.objects.count()
        business_count = Business.objects.filter(archived=False,approval=True).count()
        place_count = Place.objects.exclude(archived=True).count()

        context = {
            'business_count': business_count,
            'user_count': user_count,
            'place_count': place_count,
            'total_visitors': total_visitors,
            'all_businesses': all_businesses,
            'all_users': all_users,
        }
        return render(request, 'dashboard.html', context)


@login_required
def updatebusiness(request, pk):
    excluded_groups = ['Business', 'Admin']
    if not any(request.user.groups.filter(name=group).exists() for group in excluded_groups):
        return HttpResponseForbidden("You don't have permission to access this page.")
    else:
        business = get_object_or_404(Business, pk=pk)

        if request.POST:  # Use request.method == 'POST' for clarity
            form = BusinessUpdForm(request.POST, request.FILES, instance=business)
            if form.is_valid():
                business = form.save(commit=False)
                form.instance.categories.set(form.cleaned_data['categories'])
                business.save()

                if 'photos' in request.FILES:
                    if business.photos.exists():
                        for old_photos in business.photos.all():
                            old_photos.file.delete(save=False)  # Optionally delete files from filesystem
                            old_photos.delete()  # Remove photo
                    photos = request.FILES.getlist('photos')
                    for photos in photos:
                        photo_instance = Media(file=photos)
                        photo_instance.save()
                        business.photos.add(photo_instance)
                        business.save()

                # Check for user groups and redirect accordingly
                if request.user.groups.filter(name='Admin').exists():
                    return redirect('businessadmin')
                else:
                    return redirect('businesslist')
            else:
                # Debugging output if form is not valid
                print("Form errors:", form.errors)
        else:
            form = BusinessUpdForm(instance=business)

        context = {'form': form, 'business': business}
    return render(request, 'updatebusiness.html', context)


    
@login_required
def  deletebusiness(request,pk):
    excluded_groups = ['Business', 'Admin']
    user_groups = request.user.groups.values_list('name', flat=True)
    if not any(request.user.groups.filter(name=group).exists() for group in excluded_groups):
        return HttpResponseForbidden("You don't have permission to access this page.")
    else:
        business = get_object_or_404(Business, pk=pk)
        if request.POST:
            business.archived = True
            business.save()  
            if 'Admin' in user_groups:
                return redirect('businessadmin')
            elif 'Business' in user_groups:
                return redirect('businesslist')
        context={'business':business}
        return render(request,'deletebusiness.html',context)


def businesssign(request):
    if request.method == 'POST':
        form = BusinessForm(request.POST or  None)
        if form.is_valid():
            form.save()
        return redirect('login')
    return render(request, 'businesssign.html',{})        

@login_required
def placelist(request):
    if not request.user.groups.filter(name='Admin').exists():
        return HttpResponseForbidden("You don't have permission to access this page.")
    else:
       all_admin = Place.objects.all
       context = {'all_admin':all_admin}
       return render(request, 'placelist.html',context)  

@login_required
def updatePlace(request,pk):
    if not request.user.groups.filter(name='Admin').exists():
        return HttpResponseForbidden("You don't have permission to access this page.")
    else:
        place = get_object_or_404(Place, pk=pk)
        

        if request.POST:
            form = PlaceForm(request.POST, request.FILES, instance=place)
            if form.is_valid():
                place = form.save(commit=False)
                form.instance.categories.set(form.cleaned_data['categories'])
                place.save()

                if 'photo' in request.FILES:
                # Remove old photos if needed
                    if place.photo.exists():
                        for old_photo in place.photo.all():
                            old_photo.file.delete(save=False)  # Optionally delete files from filesystem
                            old_photo.delete()  # Remove photo
                    photos = request.FILES.getlist('photo')
                    for photo in photos:
                        photo_instance = PlaceMedia(file=photo)
                        photo_instance.save()
                        place.photo.add(photo_instance)

                return redirect('placelist')
        else:
            form = PlaceForm(instance=place)

        context = {'form': form, 'place': place} 
        return render(request, 'updateplace.html', context)
@login_required
def  deleteplace(request,pk):
    if not request.user.groups.filter(name='Admin').exists():
        return HttpResponseForbidden("You don't have permission to access this page.")
    else:
        place = get_object_or_404(Place, pk=pk)
        if request.POST:
            place.archived = True
            place.save()
            return redirect('placelist')
        context={'item':place}
        return render(request,'deleteplace.html',context)

@login_required
def approvallist(request):
    if not request.user.groups.filter(name='Admin').exists():
        return HttpResponseForbidden("You don't have permission to access this page.")
    else:        
        all_approval = Business.objects.filter(approval=False)
        all_approval1 = Business.objects.filter(approval=False)
        print(all_approval1)  
        context = {'all_approval':all_approval, 'all_approval1':all_approval1}
        return render(request, 'approval.html',context)

@login_required
def declinebusiness(request,pk):
    if not request.user.groups.filter(name='Admin').exists():
        return HttpResponseForbidden("You don't have permission to access this page.")
    else:
        business = get_object_or_404(Business, pk=pk)
        if request.POST:
            user = User.objects.get(username=business.username)
            business.delete()
            user.delete()
            return redirect('approvallist')
        context={'business':business}
        return render(request,'decline.html',context)
    
@login_required    
def approvebusiness(request,pk):
    if not request.user.groups.filter(name='Admin').exists():
        return HttpResponseForbidden("You don't have permission to access this page.")
    else:
        business = get_object_or_404(Business, pk=pk)
        if request.POST:
            business.approval = True
            business.save()
            return redirect('approvallist')
        context={'business':business}
        return render(request,'approve.html',context)
    
def viewplace(request,pk):
       place = get_object_or_404(Place, pk=pk)
       context = {'place':place}
       return render(request, 'viewplace.html',context)  
    
def viewbusiness(request,pk):
       business = get_object_or_404(Business, pk=pk)
       context = {'business':business}
       return render(request, 'viewbusiness.html',context)

def bussdeets(request,pk):
    business = get_object_or_404(Business, pk=pk)
    form = BusinessUpdForm(instance=business)
    photos = request.FILES.getlist('photos')
    for photos in photos:
            photo_instance = Media(file=photos)
            photo_instance.save()
            business.photos.add(photo_instance)
    context = {'business':business,'form':form}
    return render(request, 'bussdeets.html',context)


@login_required
def itinerary(request):
    if not request.user.groups.filter(name='NormalUsers').exists():
        return HttpResponseForbidden("You don't have permission to access this page.")
    else:
         place = Place.objects.all
         business = Business.objects.all
         context = {'place':place,'business': business}
         return render(request, 'itinerary.html',context)
        

def placepopup(request):
    places = Place.objects.all()
    businesses = Business.objects.all()
    return render(request, 'popup_template.html', {'places': places, 'businesses': businesses})


def update_place(request, place_id):
    if request.method == 'POST':
        place = Place.objects.get(pk=place_id)
        place.name = request.POST.get('name')
        place.picture = request.FILES.get('picture')
        place.save()


@login_required
def declinebus(request,pk):
    if not request.user.groups.filter(name='Admin').exists():
        return HttpResponseForbidden("You don't have permission to access this page.")
    else:
        business = get_object_or_404(Business, pk=pk)
        if request.POST:
            user = User.objects.get(username=business.username)
            business.delete()
            user.delete()
            return redirect('approvallist')
        context={'business':business}
        return render(request,'declinebus.html',context)
    

@login_required
def deleteowner(request,pk):
    if not request.user.groups.filter(name='Admin').exists():
        return HttpResponseForbidden("You don't have permission to access this page.")
    else:
        business = get_object_or_404(Business, pk=pk)
        if request.POST:
            user = User.objects.get(username=business.username)
            business.delete()
            user.delete()
            return redirect('dashboard')
        context={'business':business}
        return render(request,'deleteowner.html',context)
    

@login_required
def deletevisitor(request,pk):
    if not request.user.groups.filter(name='Admin').exists():
        return HttpResponseForbidden("You don't have permission to access this page.")
    else:
        user = get_object_or_404(NormalUser, pk=pk)
        if request.POST:
            user = NormalUser.objects.get(username=user.username)
            user.delete()
            return redirect('dashboard')
        context={'user':user}
        return render(request,'deletevisitor.html',context)
    
@login_required    
def approvebus(request,pk):
    if not request.user.groups.filter(name='Admin').exists():
        return HttpResponseForbidden("You don't have permission to access this page.")
    else:
        business = get_object_or_404(Business, pk=pk)
        if request.POST:
            business.approval = True
            business.save()
            return redirect('approvallist')
        context={'business':business}
        return render(request,'approvebus.html',context)

@login_required
@csrf_exempt
def save_itinerary_state(request):
    if request.method == 'POST' and request.user.is_authenticated:
        data = json.loads(request.body)
        places = data.get('places', [])
        text = data.get('text', [])
        images = data.get('images', [])
        place_ids = data.get('placeIds', [])
        types = data.get('types', [])
        start_time = data.get('startTime', '')
        budget = data.get('budget', [])
        times = data.get('times', [])
        times2 = data.get('times2', [])
        category = data.get('category', [])
        # Save the itinerary state to the database
        ItineraryState.objects.update_or_create(user=request.user, defaults={'places': places, 'times': times,'times2': times2,'images':images,'place_ids': place_ids,'types': types,"start_time":start_time,"budget":budget,"text":text,"category":category})
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required
def load_itinerary_state(request):
    if request.user.is_authenticated:
        itinerary_state = ItineraryState.objects.filter(user=request.user).first()
        if itinerary_state:
            data = {'places': itinerary_state.places, 'times': itinerary_state.times,'times2': itinerary_state.times2,'images':itinerary_state.images,'placeIds': itinerary_state.place_ids,'types': itinerary_state.types,'startTime': itinerary_state.start_time.strftime('%H:%M'),'budget':itinerary_state.budget,'text':itinerary_state.text,'category':itinerary_state.category}
            return JsonResponse(data)
    return JsonResponse({'places': [], 'times': [],'times2': [], 'images': [],'placeIds': [],'types': [], 'startTime': '','budget': [],'text': [],'category': []})


def map(request):
    return render(request, 'map.html', {})

@login_required
def adpromo(request):
    if not request.user.groups.filter(name='Admin').exists():
        return HttpResponseForbidden("You don't have permission to access this page.")
    else:
      all_admin = Place.objects.all()
      context = {'all_admin': all_admin,} 
      return render(request,'adpromo.html',context)




@login_required
def promo(request,pk):
    if not request.user.groups.filter(name='Admin').exists():
        return HttpResponseForbidden("You don't have permission to access this page.")
    else:
        all_admin = Place.objects.all()
        place = get_object_or_404(Place, pk=pk)
        
        if request.POST:
            form = PromoForm(request.POST,request.FILES,instance=place)
            if form.is_valid():
                place = form.save(commit=False)
                place.save()
                return redirect('adpromo')
        else:
            form = PromoForm(instance=place)

        context = {'form': form, 'place': place,'all_admin': all_admin} 
        return render(request, 'promo.html', context)

    




    


   



    






