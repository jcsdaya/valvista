from django.urls import path,include
from. import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
  path('login_business',views.login_business,name="login_business"),
  path('register_business',views.register_business,name="register_business"),
  path('logout_business',views.logout_business,name="logout_business"),
  
  
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)