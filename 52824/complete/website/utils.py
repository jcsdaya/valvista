from .models import Place, Favorite
from business.models import Business

def get_home_context(user):
    all_admin = Place.objects.all()
    all_business = Business.objects.all()
    
    favorite_places = []
    favorite_businesses = []

    if user.is_authenticated:
        user_favorites = Favorite.objects.filter(user=user)
        favorite_places = user_favorites.filter(place__isnull=False).values_list('place_id', flat=True)
        favorite_businesses = user_favorites.filter(business__isnull=False).values_list('business_id', flat=True)
    
    places_with_ratings = []
    for place in all_admin:
        places_with_ratings.append({
            'place': place,
            'average_rating': place.average_rating(),
        })
    
    context = {
        'all_admin': all_admin,
        'all_business': all_business,
        'favorite_places': favorite_places,
        'favorite_businesses': favorite_businesses,
        'places_with_ratings': places_with_ratings,
    }
    return context


