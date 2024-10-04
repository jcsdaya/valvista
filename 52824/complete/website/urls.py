from django.urls import path
from. import views
from django.conf import settings
from django.conf.urls.static import static
from .views import logout_view

urlpatterns = [
  path('home/',views.home,name="home"),
  path('login/',views.loginuser,name="login"),
  path('logout/', logout_view, name='logout'),
  path('register/',views.register,name="register"),
  path('addplace/',views.addplace,name="addplace"),
  path('userhome/',views.userhome,name="userhome"),
  path('businesshome/',views.businesshome,name="businesshome"),
  path('adminhome/',views.adminhome,name="adminhome"),
  path('archives/',views.archives,name="archives"),
  path('admindelete/<str:pk>/',views.admindelete,name="admindelete"),
  path('businesssign/',views.businesssign,name="businesssign"),
  path('businessadmin/',views.businessadmin,name="businessadmin"),
  path('businesslist/',views.businesslist,name="businesslist"),
  path('placelist/',views.placelist,name="placelist"),
  path('updatePlace/<str:pk>/', views.updatePlace, name="updatePlace"),
  path('updatebusiness/<str:pk>/', views.updatebusiness, name="updatebusiness"),
  path('deletebusiness/<str:pk>/', views.deletebusiness, name="deletebusiness"),
  path('deleteplace/<str:pk>/', views.deleteplace, name="deleteplace"),
  path('approval/', views.approvallist, name="approvallist"),
  path('approve/<str:pk>/', views.approvebusiness, name="approvebusiness"),
  path('decline/<str:pk>/', views.declinebusiness, name="declinebusiness"),
  path('approvebus/<str:pk>/', views.approvebus, name='approvebus'),
  path('declinebus/<str:pk>/', views.declinebus, name='declinebus'),
  path('dashboard', views.dashboard, name="dashboard"),
  path('viewplace/<str:pk>/', views.viewplace, name="viewplace"),
  path('viewbusiness/<str:pk>/', views.viewbusiness, name="viewbusiness"),
  path('add_favorite_place/<int:place_id>/', views.add_favorite_place, name='add_favorite_place'),
  path('add_favorite_business/<int:business_id>/', views.add_favorite_business, name='add_favorite_business'),
  path('favorites/', views.favorite_list, name='favorite_list'),
  path('itinerary/', views.itinerary, name='itinerary'),
  path('save_itinerary_state/', views.save_itinerary_state, name='save_itinerary_state'),
  path('load_itinerary_state/', views.load_itinerary_state, name='load_itinerary_state'),
  path('deleteowner/<str:pk>/', views.deleteowner, name="deleteowner"),
  path('deletevisitor/<str:pk>/', views.deletevisitor, name="deletevisitor"),
  path('viewrating/<str:pk>/', views.viewrating, name="viewrating"),
  path('ratingform/<int:place_id>', views.ratingform, name='ratingform'),
  path('businessrating/<int:buss_id>', views.businessrating, name='businessrating'),
  path('bussdeets/<str:pk>/', views.bussdeets, name="bussdeets"),
  path('map/',views.map,name="map"),
  path('adpromo',views.adpromo,name="adpromo"),
  path('promo/<str:pk>/',views.promo, name="promo"),
  path('success',views.success,name="success")

  
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)