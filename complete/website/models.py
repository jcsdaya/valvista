from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User,Group
from business.models import Business,BusinessDetails
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Admin(models.Model):
        username = models.CharField (max_length=50,unique=True)
        email = models.EmailField(max_length=100)
        password = models.CharField (max_length=50)

        def __str__ (self):
            return self.username
        
class Place(models.Model):
        CATEGORY_CHOICES = [
        ('Leisure', 'Leisure'),
        ('Educational', 'Educational'),
        ('Historical', 'Historical'),
        ('Diner', 'Diner'),
        ]
        COST_CHOICES = [
        ('0','0'),
        ('1-200','1-200'),
        ('201-500','201-500'),
        ('501+','501+'),     
        ]
        name = models.CharField (max_length=100)
        location = models.CharField (max_length=100)
        description = models.CharField (max_length=1000)
        category = models.CharField (max_length=100,default='Leisure',choices=CATEGORY_CHOICES)
        category2 = models.CharField (max_length=100, blank=True,null=True,choices=CATEGORY_CHOICES)
        category3 = models.CharField (max_length=100, blank=True,null=True,choices=CATEGORY_CHOICES)
        time = models.CharField (max_length=20)
        timeclose = models.CharField (max_length=20)
        cost = models.CharField(max_length=100, blank=True,null=True,choices= COST_CHOICES)
        photo = models.ImageField(upload_to="media",blank=True,null=True)
        photos = models.ImageField(upload_to="media", blank=True,null=True)
        thumbnail = models.ImageField(upload_to="media")
        archived = models.BooleanField(default=False)
        map = models.CharField(max_length=2000,blank=True,null=True)
        promos = models.ImageField(upload_to="media",blank=True,null=True)
        announcement = models.TextField(max_length=5000, blank=True,null=True)
        
        def average_rating(self):
            ratings = Rating.objects.filter(content_type=ContentType.objects.get_for_model(self), object_id=self.id)
            if ratings.exists():
                return sum([rating.score for rating in ratings]) / ratings.count()
            return 0
        
        def __str__ (self):
                return self.name
        
class NormalUser(models.Model):
       username = models.CharField (max_length=50,unique=True)
       favorites = models.TextField(blank=True,null=True)
       email = models.EmailField (max_length=50)
       password = models.CharField (max_length=50)

       
       def __str__ (self):
                return self.email
       
@receiver(post_save, sender=NormalUser)
def create_user(sender, instance, created, **kwargs):
    if created:
        user = User.objects.create_user(username=instance.username, password=str(instance.password))

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
    business = models.ForeignKey(BusinessDetails, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'place', 'business')


class Rating(models.Model):
    user = models.ForeignKey(NormalUser, on_delete=models.CASCADE)
    score = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f'{self.content_object} - {self.score}'


class Itinerary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    places = models.ManyToManyField(Place)
    businesses=models.ManyToManyField(BusinessDetails)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Itinerary {self.id}"
    

class ItineraryState(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    places = models.JSONField(default=list)
    times = models.JSONField(default=list)
    images = models.JSONField(default=list)
    place_ids = models.JSONField(default=list)
    types = models.JSONField(default=list)

    def __str__(self):
        return f"Itinerary State for {self.user.username}"

class FavoriteItinerary(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='favorite_itinerary')
    itinerary_state = models.OneToOneField(ItineraryState, on_delete=models.CASCADE, related_name='favorite_itinerary')

    def __str__(self):
        return f"Favorite Itinerary for {self.user.username}"



