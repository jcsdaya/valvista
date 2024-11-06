from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User,Group
from business.models import Business
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
import os
from django.utils import timezone

class Admin(models.Model):
        username = models.CharField (max_length=50,unique=True)
        email = models.EmailField(max_length=100)
        password = models.CharField (max_length=50)

        def __str__ (self):
            return self.username
        
class PlaceMedia(models.Model):
    file = models.FileField(upload_to="media")

@receiver(models.signals.pre_save, sender=PlaceMedia)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = PlaceMedia.objects.get(pk=instance.pk).file
    except PlaceMedia.DoesNotExist:
        return False

    new_file = instance.file
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


class Place(models.Model):
        COST_CHOICES = [
        ('0','0'),
        ('1-200','1-200'),
        ('201-500','201-500'),
        ('501+','501+'),     
        ]
        STATUS_CHOICES = [
        ('Open','Open'),
        ('Closed','Closed'),
        ('Temporarily Closed','Temporarily Closed'),
        ('For Renovation','For Renovation'),     
        ]
        name = models.CharField (max_length=100)
        location = models.CharField (max_length=100)
        description = models.CharField (max_length=1000)
        categories = models.ManyToManyField('Category', related_name='places')
        time = models.CharField (max_length=20)
        timeclose = models.CharField (max_length=20)
        cost = models.CharField(max_length=100, blank=True,null=True,choices= COST_CHOICES)
        photo = models.ManyToManyField(PlaceMedia,related_name='places',blank=True)
        thumbnail = models.ImageField(upload_to="media")
        archived = models.BooleanField(default=False)
        map = models.CharField(max_length=2000,blank=True,null=True)
        promos = models.ImageField(upload_to="media",blank=True,null=True)
        announcement = models.TextField(max_length=5000, blank=True,null=True)
        status = models.CharField(max_length=100, blank=True,null=True,choices= STATUS_CHOICES)
        lat = models.DecimalField(max_digits=30, decimal_places=20, blank=True, null=True)
        lng = models.DecimalField(max_digits=30, decimal_places=20, blank=True, null=True)
        
        
        def __str__ (self):
                return self.name

class Rating(models.Model):
    place = models.ForeignKey(Place, related_name='ratings', on_delete=models.CASCADE,null=True, blank=True)
    name = models.CharField(max_length=100,null=True, blank=True)
    score = models.IntegerField(choices=[(i, f"{i} Star") for i in range(1, 6)])
    comment = models.TextField(max_length=1000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['place', 'name'], name='unique_place_name')
        ]
        
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    

        
class NormalUser(models.Model):
       username = models.CharField (max_length=50,unique=True,null=True)
       favorites = models.TextField(blank=True,null=True)
       email = models.EmailField (max_length=50, unique=True)
       password = models.CharField (max_length=50)

       
       def __str__ (self):
                return self.email
       
@receiver(post_save, sender=NormalUser)
def create_user(sender, instance, created, **kwargs):
    if created:
        user = User.objects.create_user(username=instance.username, password=str(instance.password),email=str(instance.email))

        group_name = 'NormalUsers'
        group, created = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)

class Visitor(models.Model):
    ip_address = models.CharField(max_length=45)
    user_agent = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, null=True, blank=True, on_delete=models.CASCADE)
    business = models.ForeignKey(Business, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'place', 'business')



class Itinerary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    places = models.ManyToManyField(Place)
    businesses=models.ManyToManyField(Business)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Itinerary {self.id}"
    

class ItineraryState(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    places = models.JSONField(default=list)
    place_count = models.JSONField(default=list)
    times = models.JSONField(default=list)
    times2 = models.JSONField(default=list)
    images = models.JSONField(default=list)
    text = models.JSONField(default=list)
    budget = models.JSONField(default=list)
    place_ids = models.JSONField(default=list)
    types = models.JSONField(default=list)
    start_time = models.CharField(blank=True, null=True,max_length=10)
    category = models.JSONField(default=list)
    time = models.JSONField(default=list)
    timeclose = models.JSONField(default=list)

    def __str__(self):
        return f"Itinerary State for {self.user.username}"

class FavoriteItinerary(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='favorite_itinerary')
    itinerary_state = models.OneToOneField(ItineraryState, on_delete=models.CASCADE, related_name='favorite_itinerary')

    def __str__(self):
        return f"Favorite Itinerary for {self.user.username}"
    

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    placeid = models.CharField(max_length=255,null=True)
    businessid = models.CharField(max_length=255,null=True)
    created_at = models.DateTimeField(default=timezone.now)
    origin = models.CharField(max_length=50, default="place")
    
    def __str__(self):
        return f"Notification for {self.user} - {self.message}"





