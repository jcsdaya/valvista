from .models import Place, Favorite
from business.models import Business
from django.db.models import Avg, Count
from django.shortcuts import render


def get_home_context(user):
    
    favorite_places = []
    favorite_businesses = []

    places = Place.objects.annotate(
        avg_rating=Avg('ratings__score'),  
        rating_count=Count('ratings')      
    )

    business = Business.objects.annotate(
        avg_rating=Avg('ratings__score'),  
        rating_count=Count('ratings')      
    )

    if user.is_authenticated:
        user_favorites = Favorite.objects.filter(user=user)
        favorite_places = user_favorites.filter(place__isnull=False).values_list('place_id', flat=True)
        favorite_businesses = user_favorites.filter(business__isnull=False).values_list('business_id', flat=True)
    

    
    context = {
        'all_admin': places,
        'all_business': business,
        'favorite_places': favorite_places,
        'favorite_businesses': favorite_businesses,


    }
    return context


