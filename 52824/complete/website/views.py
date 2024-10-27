from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import SignupForm,PlaceForm,PromoForm,BusPromoForm,RatingForm
from business.forms import BusinessForm,BusinessUpdForm,BusinessRating
from .models import Place,NormalUser,Visitor,Favorite,ItineraryState,PlaceMedia
from business.models import Business,Media
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from .utils import get_home_context
from django.urls import reverse
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
import qrcode
from django.db.models import Avg, Count
from django.contrib.auth.hashers import make_password



 
def home(request):
    excluded_groups = ['Business', 'Admin']
    if any(request.user.groups.filter(name=group).exists() for group in excluded_groups):
        return redirect('login')
    else:
        context = get_home_context(request.user)
        return render(request, 'home.html', context)


def ratingform(request,place_id):
    place = get_object_or_404(Place, id=place_id) 
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.user = request.user  # Set the user who is rating
            rating.place = place 
            rating.save()
            messages.success(request, 'Your rating has been submitted successfully!')
            return redirect('ratingform', place_id=place_id)
    else:
        form = RatingForm()
    
    return render(request, 'rating.html', {'form': form,'place': place})

def businessrating(request,buss_id):
    business = get_object_or_404(Business, id=buss_id) 
    if request.method == 'POST':
        form = BusinessRating(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.user = request.user  # Set the user who is rating
            rating.business = business 
            rating.save()
            messages.success(request, 'Your rating has been submitted successfully!')
            return redirect('businessrating', buss_id=buss_id)  # Redirect to a success page or the place page
    else:
        form = BusinessRating()
    
    return render(request, 'businessrating.html', {'form': form,'business': business})

@login_required
def add_favorite_place(request, place_id):
    if not request.user.groups.filter(name='NormalUsers').exists():
        return redirect('login')
    else:
        place = get_object_or_404(Place, id=place_id)
        favorite, created = Favorite.objects.get_or_create(user=request.user, place=place)

        if not created:
            favorite.delete()

        # Use 'HTTP_REFERER' to go back to the previous page
        referer = request.META.get('HTTP_REFERER', reverse('home'))

        return redirect(referer)

@login_required
def add_favorite_business(request, business_id):
    if not request.user.groups.filter(name='NormalUsers').exists():
        return redirect('login')
    else:
        business = get_object_or_404(Business, id=business_id)
        favorite, created = Favorite.objects.get_or_create(user=request.user, business=business)
        if not created:
            favorite.delete()
        if request.get_full_path() == reverse('userhome'):
            return redirect('home')  
        else:
            return redirect('home')


@login_required
def favorite_list(request):
    if not request.user.groups.filter(name='NormalUsers').exists():
        return redirect('login')
    else:
        favorites = Favorite.objects.filter(user=request.user)
        return render(request, 'favorite.html', {'favorites': favorites})
        

def loginuser(request):
    error_message=""
    if request.method =="POST":
        username = request.POST['username']
        password = request.POST['password']
        remember_me = request.POST.get('remember_me')
        user = authenticate(request, username=username, password=password)
        hashed_password = make_password(password)
        print(f"Username: {username}, Password: {hashed_password}")
        print("User object type:", type(user))
        print( remember_me)
        if user is not None:
            login(request, user)
            print(f"Authenticated User: {user}")

            if remember_me:
                request.session.set_expiry(1209600)  # 2 weeks in seconds
            else:
                request.session.set_expiry(0)  # Session expires on browser close

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
                return redirect('dashboard')
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
        return redirect('login')
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
                messages.success(request, "Place Added successfully.")
        return redirect('placelist')
    return render(request, 'addplace.html',{'form':form})

@login_required
def adminhome(request):
    if not request.user.groups.filter(name='Admin').exists():
        return redirect('login')
    else:
       all_admin = Place.objects.all
       context = {'all_admin':all_admin}
       return render(request, 'adminhome.html',context)

@login_required
def userhome(request):
    if not request.user.groups.filter(name='NormalUsers').exists():
        return redirect('login')
    else:
        context = get_home_context(request.user)
        return render(request, 'userhome.html',context)

@login_required
def businesshome(request):
    if not request.user.groups.filter(name='Business').exists():
        return redirect('login')
    
    # Fetch the Business instance related to the current user
    try:
        business = Business.objects.get(username=request.user.username)
    except Business.DoesNotExist:
        # Handle the case where the Business instance does not exist
        return HttpResponseForbidden("No associated business found.")
    
    business = get_object_or_404(Business.objects.annotate(
        avg_rating=Avg('ratings__score'), rating_count=Count('ratings')), username=request.user.username)
    ratings = business.ratings.all() 
    if request.method == 'POST':
        form = BusPromoForm(request.POST, request.FILES, instance=business)
        if form.is_valid():
            form.save()
            messages.success(request, "Announcement/Promo Posted Successfully") 
            return redirect('businesshome')
    else:
        form = BusPromoForm(instance=business)

    context = {'form': form,'business':business,'ratings':ratings}
    return render(request, 'businesshome.html', context)


@login_required
def businesslist(request):
    excluded_groups = ['Business', 'Admin']
    if not any(request.user.groups.filter(name=group).exists() for group in excluded_groups):
       return redirect('login')
    else:
        current_user_business = Business.objects.get(username=request.user.username)
        all_bus = Business.objects.filter(username=current_user_business)
        context = {'all_bus':all_bus}
        return render(request, 'businesslist.html',context) 

@login_required
def businessadmin(request):
    if not request.user.groups.filter(name='Admin').exists():
        return redirect('login')
    else:
        all_buss = Business.objects.all
        context = {'all_buss':all_buss}
        return render(request, 'businessadmin.html',context) 
    

@login_required
def  admindelete(request,pk):
    if not request.user.groups.filter(name='Admin').exists():
        return redirect('login')
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
        return redirect('login')
    else:
        all_buss = Business.objects.all
        all_admin = Place.objects.all
        context = {'all_bus':all_buss,'all_admin':all_admin}
        return render(request, 'archives.html',context) 
    
@login_required
def dashboard(request):
    if not request.user.groups.filter(name='Admin').exists():
        return redirect('login')
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
        return redirect('login')
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
                    messages.success(request, "Updated Business successfully.")
                    return redirect('businessadmin')
                else:
                    messages.success(request, "Updated Business successfully.")
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
        return redirect('login')
    else:
        business = get_object_or_404(Business, pk=pk)
        if request.POST:
            business.archived = True
            business.save()  
            if 'Admin' in user_groups:
                messages.success(request, "Business Removed successfully.")
                return redirect('businessadmin')
            elif 'Business' in user_groups:
                messages.success(request, "Business Removed successfully.")
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
         return redirect('login')
    else:
       all_admin = Place.objects.all
       context = {'all_admin':all_admin}
       return render(request, 'placelist.html',context)  

@login_required
def updatePlace(request,pk):
    if not request.user.groups.filter(name='Admin').exists():
         return redirect('login')
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
                messages.success(request, "Place updated successfully.")
                return redirect('placelist')
        else:
            form = PlaceForm(instance=place)

        context = {'form': form, 'place': place} 
        return render(request, 'updateplace.html', context)
@login_required
def  deleteplace(request,pk):
    if not request.user.groups.filter(name='Admin').exists():
        return redirect('login')
    else:
        place = get_object_or_404(Place, pk=pk)
        if request.POST:
            place.archived = True
            place.save()
            messages.success(request, "Place is deleted successfully.")
            return redirect('placelist')
        context={'item':place}
        return render(request,'deleteplace.html',context)

@login_required
def approvallist(request):
    if not request.user.groups.filter(name='Admin').exists():
        return redirect('login')
    else:        
        all_approval = Business.objects.filter(approval=False)
        all_approval1 = Business.objects.filter(approval=False)
        print(all_approval1)  
        context = {'all_approval':all_approval, 'all_approval1':all_approval1}
        return render(request, 'approval.html',context)

@login_required
def declinebusiness(request,pk):
    if not request.user.groups.filter(name='Admin').exists():
        return redirect('login')
    else:
        business = get_object_or_404(Business, pk=pk)
        if request.POST:
            user = User.objects.get(username=business.username)
            business.delete()
            user.delete()
            messages.success(request, "Business Denied successfully.")
            return redirect('approvallist')
        context={'business':business}
        return render(request,'decline.html',context)
    
@login_required    
def approvebusiness(request,pk):
    if not request.user.groups.filter(name='Admin').exists():
        return redirect('login')
    else:
        business = get_object_or_404(Business, pk=pk)
        if request.POST:
            business.approval = True
            business.save()
            messages.success(request, "Business Approved successfully.")
            return redirect('approvallist')
        context={'business':business}
        return render(request,'approve.html',context)
    
def viewplace(request,pk):
    excluded_groups = ['Business', 'Admin']
    if any(request.user.groups.filter(name=group).exists() for group in excluded_groups):
        return redirect('login')
    else:
        place = get_object_or_404(Place.objects.annotate(
            avg_rating=Avg('ratings__score'), rating_count=Count('ratings')), pk=pk)

        ratings = place.ratings.all() 
        context = {
            'place': place,
            'ratings': ratings,
            'avg_rating': place.avg_rating,  
            'rating_count': place.rating_count  
            }
        return render(request, 'viewplace.html',context)  
    
def viewbusiness(request,pk):
    excluded_groups = ['Business', 'Admin']
    if any(request.user.groups.filter(name=group).exists() for group in excluded_groups):
        return redirect('login')
    else:
        business = get_object_or_404(Business.objects.annotate(
            avg_rating=Avg('ratings__score'), rating_count=Count('ratings')), pk=pk)

        ratings = business.ratings.all() 
        context = {
            'business': business,
            'ratings': ratings,
            'avg_rating': business.avg_rating,  
            'rating_count': business.rating_count  
            }
        return render(request, 'viewbusiness.html',context) 


@login_required
def bussdeets(request,pk):
    if not request.user.groups.filter(name='Admin').exists():
        return redirect('login')
    else:
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
        return redirect('login')
    else:
         place = Place.objects.all
         business = Business.objects.all

         place_times = set(place.time for place in Place.objects.all())
         business_times = set(business.time for business in Business.objects.all())
    
    
         combined_times = sorted(place_times.union(business_times))
         context = {'place':place,'business': business, 'combined_times': combined_times}
         return render(request, 'itinerary.html',context)


@login_required
def declinebus(request,pk):
    if not request.user.groups.filter(name='Admin').exists():
        return redirect('login')
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
        return redirect('login')
    else:
        business = get_object_or_404(Business, pk=pk)
        if request.POST:
            user = User.objects.get(username=business.username)
            business.delete()
            user.delete()
            messages.success(request, "Business Owner deleted successfully.")
            return redirect('dashboard')
        context={'business':business}
        return render(request,'deleteowner.html',context)
    

@login_required
def deletevisitor(request,pk):
    if not request.user.groups.filter(name='Admin').exists():
        return redirect('login')
    else:
        user = get_object_or_404(NormalUser, pk=pk)
        if request.POST:
            user = User.objects.get(username=user.username)
            user.delete()
            messages.success(request, "Visitor account deleted successfully.")
            return redirect('dashboard')
        context={'user':user}
        return render(request,'deletevisitor.html',context)
    
@login_required    
def approvebus(request,pk):
    if not request.user.groups.filter(name='Admin').exists():
        return redirect('login')
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
        place_count = data.get('placeCount', 5) 
        text = data.get('text', [])
        images = data.get('images', [])
        place_ids = data.get('placeIds', [])
        types = data.get('types', [])
        start_time = data.get('startTime', '')
        budget = data.get('budget', [])
        times = data.get('times', [])
        times2 = data.get('times2', [])
        category = data.get('category', [])
        time = data.get('time', [])
        timeclose = data.get('timeclose', [])
        # Save the itinerary state to the database
        ItineraryState.objects.update_or_create(user=request.user, defaults={'places': places, 'place_count': place_count, 'times': times,'times2': times2,'time': time,'timeclose': timeclose,'images':images,'place_ids': place_ids,'types': types,"start_time":start_time,"budget":budget,"text":text,"category":category})
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required
def load_itinerary_state(request):
    if request.user.is_authenticated:
        itinerary_state = ItineraryState.objects.filter(user=request.user).first()
        if itinerary_state:
            data = {'places': itinerary_state.places,'placeCount': itinerary_state.place_count, 'times': itinerary_state.times,'times2': itinerary_state.times2,'time': itinerary_state.time,'timeclose': itinerary_state.timeclose,'images':itinerary_state.images,'placeIds': itinerary_state.place_ids,'types': itinerary_state.types,'startTime': itinerary_state.start_time,'budget':itinerary_state.budget,'text':itinerary_state.text,'category':itinerary_state.category}
            return JsonResponse(data)
    return JsonResponse({'places': [],'place_count': [], 'times': [],'times2': [],'time': [],'timeclose': [], 'images': [],'placeIds': [],'types': [], 'startTime': '','budget': [],'text': [],'category': []})


def map(request):
    return render(request, 'map.html', {})

@login_required
def adpromo(request):
    if not request.user.groups.filter(name='Admin').exists():
        return redirect('login')
    else:
      all_admin = Place.objects.all()
      context = {'all_admin': all_admin,} 
      return render(request,'adpromo.html',context)

def success(request):

    return render(request,'success.html')



@login_required
def promo(request,pk):
    if not request.user.groups.filter(name='Admin').exists():
        return redirect('login')
    else:
        all_admin = Place.objects.all()
        place = get_object_or_404(Place.objects.annotate(
        avg_rating=Avg('ratings__score'), rating_count=Count('ratings')), pk=pk)
        ratings = place.ratings.all() 
        
        if request.POST:
            form = PromoForm(request.POST,request.FILES,instance=place)
            if form.is_valid():
                place = form.save(commit=False)
                place.save()
                messages.success(request, "Promo added successfully.")
                return redirect('adpromo')
        else:
            form = PromoForm(instance=place)

        context = {'form': form, 'place': place,'all_admin': all_admin,'ratings':ratings} 
        return render(request, 'promo.html', context)
    







    


   



    






