from django.contrib import admin
from .models import Admin
from .models import Place
from .models import NormalUser,Itinerary, Rating



admin.site.register(Admin)
admin.site.register(NormalUser)
admin.site.register(Place)
admin.site.register(Itinerary)
admin.site.register(Rating)






